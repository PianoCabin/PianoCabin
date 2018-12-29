from utils.utils import *
from admin_end.models import *
from datetime import datetime
from django.db import transaction
from django.template.loader import get_template
from django.shortcuts import render
from urllib import parse
from io import BytesIO
import json
import jwt
import requests
import uuid
import django
import qrcode
import base64
import random
import string
import socket


# Create your views here.
class Login(APIView):
    # login API
    def get(self):
        self.getUserBySession()

    def post(self):
        self.checkMsg('code')
        code = self.msg.get('code')
        data = {
            'appid': CONFIGS['APP_ID'],
            'secret': CONFIGS['APP_SECRET'],
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        res = requests.get(url='https://api.weixin.qq.com/sns/jscode2session', params=data)
        res = json.loads(res.text)
        if 'openid' not in res:
            raise MsgError(msg='微信code无效')
        else:
            open_id = res['openid']
            user = get_or_none(User, open_id=res['openid'])
            if user is None:
                payload = {
                    'iat': datetime.utcnow(),
                    'iss': 'PianoCabin',
                    'openid': open_id
                }
                session = jwt.encode(payload=payload, key=CONFIGS['APP_SECRET'], algorithm='HS256').decode()
                user_id = ''.join(str(uuid.uuid3(uuid.NAMESPACE_DNS, open_id)).split('-'))
                user = User.objects.create(open_id=open_id, session=session, user_id=user_id)
                if user is None:
                    raise MsgError(msg='创建用户失败')
                redis_manage.session_user.set(session, user.id)
            return {'session': user.session}


class Bind(APIView):
    # bind API

    @classmethod
    def getPersonalInfo(cls, request):
        if request.method == 'GET':
            ticket = request.GET.get('ticket')
            msg = {
                'code': 1,
                'msg': '',
                'data': None
            }
            data = {}
            if not ticket:
                msg['code'] = 0
                msg['msg'] = 'No ticket'
                return render(request, 'bind.html', {'msg': json.dumps(msg)})
            url = 'https://id-tsinghua-test.iterator-traits.com/thuser/authapi/checkticket/'
            url = parse.urljoin(url, CONFIGS['THU_APP_ID']) + '/'
            url = parse.urljoin(url, ticket) + '/'
            url = parse.urljoin(url, CONFIGS['IP'].replace('.', '_')) + '/'
            res = requests.get(url=url)
            try:
                res = res.text.split(':')
                info = {}
                for text in res:
                    text = text.split('=')
                    if len(text) == 2:
                        info[text[0]] = text[1]
                    elif len(text) == 1:
                        info[text[0]] = None
                if info.get('code') != '0':
                    raise MsgError(msg='获取用户信息失败')
                else:
                    data['identity'] = info.get('zjh')
                    data['name'] = info.get('xm')
                    if info.get('yhlb') in ['J0000', 'H0000', 'J0054']:
                        data['permission'] = 1
                    elif info.get('yhlb') in ['X0011', 'X0021', 'X0031']:
                        data['permission'] = 2
                    sign = cls.getSign(data)
                    data['sign'] = sign
                    msg['data'] = data
                    return render(request, 'bind.html', {'msg': json.dumps(msg)})
            except:
                msg['code'] = 0
                msg['msg'] = 'Error'
                return render(request, 'bind.html', {'msg': json.dumps(msg)})

    def post(self):
        self.checkMsg('user_info', 'authorization')
        info = self.msg.get('user_info')
        user = self.getUserBySession()
        if user.permission != 0 or user.identity is not None:
            raise MsgError(msg='用户已绑定')
        sign = info.pop('sign')
        if sign != self.getSign(info):
            raise MsgError(msg='验证信息无效')
        user.identity = info.get('identity')
        user.permission = info.get('permission')
        user.name = info.get('name')
        user.save()


class BindInfo(APIView):
    def get(self):
        self.checkMsg('authorization')
        user = self.getUserBySession()
        return {'identity': user.identity, 'name': user.name, 'permission': user.permission}


class OrderList(APIView):
    # order/list API

    def get(self):
        self.checkMsg('authorization')
        user = self.getUserBySession()
        if self.msg.get('order_id'):
            order_list = user.order_set.filter(order_id=self.msg.get('order_id'))
        else:
            order_list = user.order_set.all()
        data = []
        for order in order_list:
            code = qrcode.QRCode(version=5)
            code.add_data(order.order_id)
            code.make()
            buffer = BytesIO()
            code.make_image().save(buffer, format='PNG')
            code_base = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode()
            if order.user.identity is not None:
                user_id = order.user.identity
            else:
                user_id = order.user.user_id
            data.append({
                'piano_type': order.piano_room.piano_type,
                'brand': order.piano_room.brand,
                'room_num': order.piano_room.room_num,
                'start_time': order.start_time.timestamp(),
                'end_time': order.end_time.timestamp(),
                'price': order.price,
                'order_status': order.order_status,
                'create_time': order.create_time.timestamp(),
                'order_id': order.order_id,
                'qrcode': code_base,
                'user_id': user_id,
                'cancel_reason': order.cancel_reason
            })
        return {"order_list": data}


class CreateFeedBack(APIView):
    # feedback API

    def post(self):
        self.checkMsg('feedback_title', 'feedback_content', 'authorization')
        user = self.getUserBySession()
        try:
            feedback = Feedback(
                user=user,
                feedback_title=self.msg.get('feedback_title'),
                feedback_content=self.msg.get('feedback_content'),
                feedback_time=datetime.now()
            )
            feedback.save()
            if feedback is None:
                raise MsgError(msg='创建反馈失败')
            feedback.save()
        except:
            raise MsgError(msg='提交反馈失败')


class OrderPay(APIView):
    def post(self):
        self.checkMsg('order_id', 'form_id')
        user = self.getUserBySession()
        order = get_or_none(Order, order_id=self.msg.get('order_id'), order_status=1)
        if order is None:
            raise MsgError(msg="订单不存在")
        order.form_id = self.msg.get('form_id')
        order.save()

        # 本机IP
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 80))
        my_addr = sock.getsockname()[0]

        nonce_str = ''.join(random.sample(string.ascii_letters + string.digits, 32))
        msg = {
            'appid': CONFIGS['APP_ID'],
            'body': 'Payment',
            'mch_id': CONFIGS['MCH_ID'],
            'nonce_str': nonce_str,
            'notify_url': CONFIGS['DOMAIN'] + '/u/order/paid/',
            'openid': user.open_id,
            'out_trade_no': order.order_id,
            'spbill_create_ip': my_addr,
            'total_fee': order.price * 100,
            'trade_type': 'JSAPI',
        }
        sign = self.getSign(msg)
        msg['sign'] = sign
        unified_order_msg = get_template('unifiedorder.xml').render(msg)
        headers = {'content-type': 'text/xml'}
        res = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=unified_order_msg, headers=headers)
        res = self.parseXML(res.text)
        if res.get('return_code') == 'SUCCESS' and res.get('result_code') == 'SUCCESS':
            msg_nd = {
                'appId': CONFIGS['APP_ID'],
                'timeStamp': str(int(datetime.now().timestamp())),
                'nonceStr': nonce_str,
                'package': 'prepay_id=' + res.get('prepay_id'),
                'signType': 'MD5'
            }
            sign = self.getSign(msg_nd)
            msg_nd['paySign'] = sign
            return msg_nd
        else:
            if res['err_code'] == 'ORDERPAID':
                order.order_status = 2
                order.save()
            raise MsgError(msg=res.get('return_msg') or res.get('err_code_des'))


class OrderPaid(APIView):
    def post(self):
        result = self.request.body
        result = self.parseXML(result)
        if result.get('return_code') == 'SUCCESS' and result.get('result_code') == 'SUCCESS':
            sign = result.pop('sign')
            if sign != self.getSign(result):
                raise MsgError(msg='验证信息无效')
            order_id = result.get('out_trade_no')
            order = Order.objects.get(order_id=order_id, order_status=1)
            order.order_status = 2
            order.save()


class NewsList(APIView):
    # feedback/list API

    def post(self):
        self.checkMsg('authorization')
        self.getUserBySession()
        if 'news_id' in self.msg:
            news_list = News.objects.filter(id=self.msg['news_id'])
        else:
            news_list = News.objects.all()
        news_list = list(news_list.values())
        for ele in news_list:
            ele["publish_time"] = int(ele["publish_time"].timestamp())
        return {'news_list': news_list}


class PianoRoomList(APIView):
    # piano-rooms-list API

    def post(self):
        self.checkMsg('date', 'type', 'authorization')
        user = self.getUserBySession()
        if self.msg.get('brand'):
            rooms = PianoRoom.objects.filter(brand=self.msg.get('brand'), piano_type=self.msg.get('type'), usable=True,
                                             art_ensemble=0)
        else:
            rooms = PianoRoom.objects.filter(piano_type=self.msg.get('type'), usable=True, art_ensemble=0)

        if self.msg.get('room_num'):
            rooms = PianoRoom.objects.filter(room_num=self.msg.get('room_num'), usable=True)

        date = datetime.fromtimestamp(self.msg.get('date')).date()
        close_time = datetime(date.year, date.month, date.day, CONFIGS['CLOSE_TIME'], 0, 0).timestamp()
        open_time = datetime(date.year, date.month, date.day, CONFIGS['OPEN_TIME'], 0, 0).timestamp()
        day = (date - datetime.now().date()).days
        sum_times = []
        if day >= CONFIGS['MAX_ORDER_DAYS'] or day < 0:
            raise MsgError(msg='非法预约日期')
        orders_rooms = {}
        for room in rooms:
            orders_rooms[room.room_num] = json.loads(redis_manage.order_list.lindex(room.room_num, day).decode())

        # 按可用时间排序
        if self.msg.get('start_time') and self.msg.get('end_time'):
            start_time = self.msg.get('start_time')
            end_time = self.msg.get('end_time')
            for room in rooms:
                orders = orders_rooms[room.room_num]
                orders.insert(0, [open_time, open_time, -1])
                orders.append([close_time, close_time, -1])
                sum_time = 0
                for i in range(len(orders) - 1):
                    if orders[i + 1][0] < start_time:
                        continue
                    if orders[i][1] > end_time:
                        break
                    sum_time += min(orders[i + 1][0], end_time) - max(orders[i][1], start_time)
                sum_times.append(sum_time)
                orders.pop()
                orders.pop(0)
            room_time = zip(sum_times, rooms)
            room_time = sorted(room_time, key=lambda x: x[0], reverse=True)
            try:
                sum_times, rooms = zip(*room_time)
            except:
                sum_times = []
                rooms = []
            rooms = list(rooms)
            for i, sum_time in enumerate(sum_times):
                if sum_time < 3600:
                    rooms[i] = None

        data = []
        for room in rooms:
            if room:
                data.append({
                    'brand': room.brand,
                    'room_num': room.room_num,
                    'unit_price': getattr(room, 'price_' + str(user.permission)),
                    'occupied_time': orders_rooms[room.room_num]
                })

        return {'room_list': data}


class OrderNormal(APIView):
    # order/normal API

    def post(self):
        self.checkMsg('room_num', 'start_time', 'end_time', 'price', 'authorization')
        user = self.getUserBySession()
        if not user.order_permission:
            raise MsgError(msg='您的预约权限被关闭，请联系管理员')
        id = 0
        try:
            with transaction.atomic():
                piano_room = get_or_none(PianoRoom, room_num=self.msg.get('room_num'), usable=True, art_ensemble=0)
                if piano_room is None:
                    raise MsgError(msg='琴房已下线或不存在，请刷新页面或联系管理员')

                # 判断时间是否合理
                start_time = datetime.fromtimestamp(self.msg.get('start_time'))
                end_time = datetime.fromtimestamp(self.msg.get('end_time'))
                open_time = datetime(start_time.year, start_time.month, start_time.day, CONFIGS['OPEN_TIME'])
                close_time = datetime(start_time.year, start_time.month, start_time.day, CONFIGS['CLOSE_TIME'])
                if start_time < datetime.now() or start_time < open_time or end_time > close_time or start_time.date() != end_time.date() or start_time > end_time:
                    raise django.db.IntegrityError

                # 计算价格是否正确
                time_elapse = end_time - start_time
                m, s = divmod(time_elapse.seconds, 60)
                h, m = divmod(m, 60)
                if m > 0:
                    h += 1
                unit_price = getattr(piano_room, 'price_' + str(user.permission))
                price = unit_price * h
                if price != self.msg.get('price'):
                    raise django.db.IntegrityError

                order = Order.objects.select_for_update().create(
                    piano_room=piano_room,
                    user=user,
                    date=start_time.date(),
                    start_time=start_time,
                    end_time=end_time,
                    create_time=datetime.now(),
                    price=self.msg.get('price'),
                )
                order.order_id = ''.join(
                    str(uuid.uuid3(uuid.NAMESPACE_DNS, str(order.id) + str(datetime.now().timestamp()))).split('-'))
                order.save()
                day = (order.date - datetime.now().date()).days
                if day >= CONFIGS['MAX_ORDER_DAYS'] or day < 0:
                    raise django.db.IntegrityError

                if redis_manage.redis_lock.acquire():
                    orders = json.loads(redis_manage.order_list.lindex(piano_room.room_num, day).decode())
                    length = len(orders)
                    for i in range(length + 1):
                        if i == length:
                            if length > 0 and order.start_time.timestamp() < orders[-1][1]:
                                raise django.db.IntegrityError
                            orders.append([order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                            break
                        if order.end_time.timestamp() <= orders[i][0]:
                            if i > 0:
                                if order.start_time.timestamp() < orders[i - 1][1]:
                                    redis_manage.redis_lock.release()
                                    raise django.db.IntegrityError
                            orders.insert(i, [order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                            break
                    orders = json.dumps(orders)
                    redis_manage.order_list.lset(piano_room.room_num, day, orders)
                    redis_manage.unpaid_orders.rpush(order.id, order.create_time.timestamp())
                    redis_manage.unpaid_orders.rpush(order.id, order.start_time.timestamp())
                    redis_manage.redis_lock.release()
                id = order.order_id
        except django.db.IntegrityError:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='无法预约，请重试')
        return {'order_id': id}


# class OrderSemester(APIView):
#     # order/semester API
#
#     def post(self):
#         self.checkMsg('room_num', 'day_in_week', 'start_time', 'end_time', 'price', 'authorization')
#         user = self.getUserBySession()
#         try:
#             with transaction.atomic():
#                 piano_room = PianoRoom.objects.select_for_update().get(room_num=self.msg.get('room_num'))
#                 order = LongTermOrder.objects.select_for_update().create(
#                     user=user,
#                     piano_room=piano_room,
#                     day_in_week=self.msg.get('day_in_week'),
#                     start_time=datetime.fromtimestamp(self.msg.get('start_time')),
#                     end_time=datetime.fromtimestamp(self.msg.get('end_time')),
#                     price=self.msg.get('price')
#                 )
#         except:
#             raise MsgError(msg='Unable to order')


class OrderChange(APIView):
    # order/change API

    def post(self):
        self.checkMsg('date', 'start_time', 'end_time', 'price', 'order_id', 'authorization')
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(order_id=self.msg.get('order_id'))

                # 判断是否已支付
                if order.order_status == 2:
                    raise django.db.IntegrityError

                # 判断时间是否合理
                start_time = datetime.fromtimestamp(self.msg.get('start_time'))
                end_time = datetime.fromtimestamp(self.msg.get('end_time'))
                open_time = datetime(start_time.year, start_time.month, start_time.day, CONFIGS['OPEN_TIME'])
                close_time = datetime(start_time.year, start_time.month, start_time.day, CONFIGS['CLOSE_TIME'])
                if start_time < datetime.now() or start_time < open_time or end_time > close_time or start_time.date() != end_time.date() or start_time > end_time:
                    raise django.db.IntegrityError

                # 计算价格是否正确
                time_elapse = end_time - start_time
                m, s = divmod(time_elapse.seconds, 60)
                h, m = divmod(m, 60)
                if m > 0:
                    h += 1
                unit_price = getattr(order.piano_room, 'price_' + str(order.user.permission))
                price = unit_price * h
                if price != self.msg.get('price'):
                    raise django.db.IntegrityError

                order.start_time = start_time
                order.end_time = end_time
                order.date = datetime.fromtimestamp(self.msg.get('date')).date()
                if order.date != start_time.date():
                    raise django.db.IntegrityError
                order.price = self.msg.get('price')
                order.save()
                if redis_manage.redis_lock.acquire():
                    day = (order.date - datetime.now().date()).days
                    room_orders = json.loads(redis_manage.order_list.lindex(order.piano_room.room_num, day).decode())
                    length = len(room_orders)
                    for i in range(length):
                        if order.id == room_orders[i][2]:
                            room_orders.pop(i)
                            break
                    length = len(room_orders)
                    for i in range(length + 1):
                        if i == length:
                            if length > 0 and order.start_time.timestamp() < room_orders[-1][1]:
                                raise django.db.IntegrityError
                            room_orders.append([order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                            break
                        if order.end_time.timestamp() <= room_orders[i][0]:
                            if i > 0:
                                if order.start_time.timestamp() < room_orders[i - 1][1]:
                                    redis_manage.redis_lock.release()
                                    raise django.db.IntegrityError
                            room_orders.insert(i, [order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                            break
                    room_orders = json.dumps(room_orders)
                    redis_manage.order_list.lset(order.piano_room.room_num, day, room_orders)
                    redis_manage.unpaid_orders.lset(order.id, 1, order.start_time)
                    redis_manage.redis_lock.release()
        except:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='无法修改订单，请重试')


class OrderCancel(APIView):
    # order/cancel API

    def post(self):
        self.checkMsg('order_id', 'authorization')
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(order_id=self.msg.get('order_id'), order_status=1)
                order.order_status = 0
                order.cancel_reason = 2
                order.save()
                if redis_manage.redis_lock.acquire():
                    day = (order.date - datetime.now().date()).days
                    room_orders = json.loads(redis_manage.order_list.lindex(order.piano_room.room_num, day).decode())
                    length = len(room_orders)
                    for i in range(length):
                        if order.id == room_orders[i][2]:
                            room_orders.pop(i)
                            break
                    room_orders = json.dumps(room_orders)
                    redis_manage.order_list.lset(order.piano_room.room_num, day, room_orders)
                    redis_manage.unpaid_orders.delete(order.id)
                    redis_manage.redis_lock.release()
        except:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='无法取消订单，请重试')
