import hashlib
import xml.etree.ElementTree as ET

from django.http import HttpResponse
from django.views.generic import View

from admin_end.models import *


class APIView(View):
    """
    API 基类
    处理基本的API转发和提供提交信息提取
    """

    def dispatch(self, request, *args, **kwargs):
        """
        :param request: Request object
        :param args: Additional arguments :class: `list <list>` object
        :param kwargs: Additional arguments :class: `dict <dict>` object
        :return: :class: `HttpResponse <HttpResponse>` object
        :rtype: HttpResponse
        """
        self.request = request
        self.msg = self.queryMsg()
        handler = getattr(self, self.request.method.lower(), None)
        if handler is None:
            return self.http_method_not_allowed()
        return self.handleMsg(handler, *args, **kwargs)

    def queryMsg(self):
        """
        提取请求体
        :return: Dictionary of submitted data
        :rtype: dict
        """
        msg = getattr(self.request, self.request.method, None)
        if msg:
            msg = msg.dict()
        else:
            msg = {}
        msg.update(self.request.FILES)
        if not msg:
            try:
                msg = json.loads(self.request.body.decode())
            except:
                msg = {}
        msg['authorization'] = self.request.META.get('HTTP_AUTHORIZATION')
        if self.request.META.get('HTTP_X_FORWARDED_FOR'):
            msg['ip'] = self.request.META.get('HTTP_X_FORWARDED_FOR')
        else:
            msg['ip'] = self.request.META.get('REMOTE_ADDR')

        return msg

    @staticmethod
    def handleMsg(handler, *args, **kwargs):
        """
        处理不同请求类型并包装返回值
        :param handler: Function of handling API interaction
        :param args: Additional arguments :class: `list <list>` object
        :param kwargs: Additional arguments :class: `dict <dict>` object
        :return: :class: `HttpResponse <HttpResponse>` object
        :rtype: HttpResponse
        """
        code = 1
        msg = ''
        data = None
        try:
            data = handler(*args, **kwargs)
        except MsgError as e:
            code = e.code
            msg = e.msg
            # print(e.msg)
        except Exception as e:
            code = 0
            msg = str(e)
            # traceback.print_exc()
        try:
            response = json.dumps({
                'code': code,
                'msg': msg,
                'data': data,
            })
        except:
            response = json.dumps({
                'code': 0,
                'msg': 'JSON Error',
                'data': None,
            })

        res = HttpResponse(response, content_type='application/json')
        # 测试用
        # res.setdefault('Access-Control-Allow-Origin', '*')
        return res

    def checkMsg(self, *keys):
        """
        检查输入
        :param keys: Additional arguments :class: `list <list>` object
        :return: None
        :rtype: None
        """
        for k in keys:
            if k not in self.msg:
                raise MsgError(msg='需要提交"%s"' % (k,))

    def checkMsgMultiOption(self, *keys):
        """
        检查多个可选输入
        :param keys: Additional arguments :class: `list <list>` object
        :return: integer
        :rtype: int
        """
        count = 0
        for k in keys:
            if k in self.msg:
                count += 1
        return count

    def getMultiOption(self, *keys):
        """
        获取不定输入
        :param keys: Additional arguments :class: `list <list>` object
        :return: :class `dict <dict>` object of existing key-value from self.msg
        :rtype: dict
        """
        msg = {}
        for k in keys:
            if k in self.msg:
                msg[k] = self.msg[k]
        return msg

    @classmethod
    def parseXML(cls, text):
        """
        解析xml
        :param text: xml string for parsing
        :return: Dictionary of the original xml string
        :rtype: dict
        """
        root = ET.fromstring(text)
        msg = dict()
        if root.tag == 'xml':
            for child in root:
                msg[child.tag] = child.text
        return msg

    @classmethod
    def getSign(cls, msg):
        """
        获取加密sign
        :param msg: Dictionary for getting message sign
        :return: string
        :rtype: str
        """
        msg_keys = list(msg.keys())
        msg_keys.sort()
        msg_str = ''
        for msg_key in msg_keys:
            msg_str += '&'
            msg_str += msg_key
            msg_str += '='
            msg_str += str(msg[msg_key])
        msg_str = msg_str[1:]
        msg_str += ('&key=' + CONFIGS['MCH_KEY'])
        md5 = hashlib.md5()
        md5.update(msg_str.encode())
        msg_str = md5.hexdigest().upper()
        return msg_str

    @classmethod
    def sendAlert(cls, send_data):
        data = {
            'grant_type': 'client_credential',
            'appid': CONFIGS['APP_ID'],
            'secret': CONFIGS['APP_SECRET'],
        }
        res = requests.get(url='https://api.weixin.qq.com/cgi-bin/token', params=data).json()
        access_token = res["access_token"]

        res = requests.post(
            url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + access_token,
            data=json.dumps(send_data)).json()
        print(res)

    def getUserBySession(self):
        """
        解析session获取用户
        :return: :class:`User <User>` object
        :rtype: User
        """
        id = redis_manage.session_user.get(self.msg['authorization'])
        if id is None:
            raise MsgError(msg='用户不存在')
        else:
            user = get_or_none(User, id=int(id.decode()))
            if user is None:
                raise MsgError(msg='用户不存在')
            else:
                return user

    def http_method_not_allowed(self, *args, **kwargs):
        return super().http_method_not_allowed(self.request, *args, **kwargs)


class MsgError(Exception):
    # 自定义的错误信息

    def __init__(self, code=0, msg='未知错误'):
        super().__init__(msg)
        self.code = code
        self.msg = msg


class TimeScheduler:
    """
    定时器任务类
    """

    @staticmethod
    def updateOrderList():
        """
        新的一天更新订单表
        :return: None
        """
        rooms = PianoRoom.objects.all()
        for room in rooms:
            date = datetime.now().date() + timedelta(days=CONFIGS['MAX_ORDER_DAYS'] - 1)
            orders = Order.objects.filter(date=date, piano_room=room, order_status__range=[1, 2]).order_by(
                'start_time')
            orders_data = []
            for order in orders:
                orders_data.append([order.start_time.timestamp(), order.end_time.timestamp(), order.id])
            orders_data = json.dumps(orders_data)
            redis_manage.order_list.lpop(room.room_num)
            redis_manage.order_list.lpush(room.room_num, orders_data)

    @staticmethod
    def updateUnpaidOrders():
        """
        十五分钟更新未支付订单
        :return: None
        """
        ids = redis_manage.unpaid_orders.keys()
        for id in ids:
            create_time = float(redis_manage.unpaid_orders.lindex(id, 0).decode())
            start_time = float(redis_manage.unpaid_orders.lindex(id, 1).decode())
            if (datetime.now().timestamp() - create_time) > CONFIGS['MAX_UNPAID_TIME'] * 60 or (
                    start_time <= datetime.now().timestamp()):
                print('execute')
                try:
                    with transaction.atomic():
                        order = Order.objects.select_for_update().get(id=int(id.decode()))
                        order.order_status = 0
                        order.cancel_reason = 1
                        order.save()
                        if redis_manage.redis_lock.acquire():
                            redis_manage.unpaid_orders.delete(id)
                            day = (datetime.now().date() - order.create_time.date()).days
                            if day == 0:
                                room_orders = redis_manage.order_list.lindex(order.piano_room.room_num, day).decode()
                                room_orders = json.loads(room_orders)
                                length = len(room_orders)
                                for i in range(length):
                                    room_order = room_orders[i]
                                    if room_order[2] == order.id:
                                        room_orders.pop(i)
                                        break
                                room_orders = json.dumps(room_orders)
                                redis_manage.order_list.lset(order.piano_room.room_num, day, room_orders)
                            redis_manage.redis_lock.release()
                except:
                    try:
                        redis_manage.redis_lock.release()
                    except:
                        pass
                    print('Unable to update order list')

    @staticmethod
    def imminentOrderAlert():
        """
        即将开始订单提醒
        :return: None
        """
        ids = redis_manage.order_list.keys()
        for id in ids:
            room_orders = redis_manage.order_list.lindex(id, 0).decode()
            room_orders = json.loads(room_orders)
            for room_order in room_orders:
                if datetime.now().timestamp() - room_order[0] < CONFIGS['ALERT_TIME'] * 60:
                    order = Order.objects.get(id=room_order[2])
                    if order.order_status == 2 and order.form_id != '':
                        APIView.sendAlert(send_data={
                            "touser": order.user.open_id,
                            "template_id": "ki8_cVjacJyR5FsfcJCOjW-kcYMtcYkAi1vIuIktVrk",
                            "form_id": order.form_id,
                            "data": {
                                "keyword1": {
                                    "value": "您预约的琴房还有" + str(
                                        int((order.start_time - datetime.now()).seconds / 60)) + "分钟开始"
                                },
                                "keyword2": {
                                    "value": order.start_time.strftime('%Y-%m-%d %X')
                                },
                                "keyword3": {
                                    "value": order.piano_room.room_num
                                },
                                "keyword4": {
                                    "value": "琴屋"
                                }
                            }
                        })

                        order.form_id = ''
                        order.save()

    def scheduledUpdate(self):
        threading.Thread(target=self.runSchedule).start()

    def runSchedule(self):
        """
        启动定时器
        :return: None
        """
        while True:
            self.updateUnpaidOrders()
            self.imminentOrderAlert()
            if datetime.now().hour == 0 and datetime.now().minute == 1:
                self.updateOrderList()
            time.sleep(1)


