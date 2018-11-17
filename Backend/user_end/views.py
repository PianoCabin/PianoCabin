from utils.utils import *
from admin_end.models import *
from datetime import datetime
from django.db import transaction
import json
import jwt
import requests
import django
from urllib import parse


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
            raise MsgError(msg='Invalid code')
        else:
            open_id = res['openid']
            payload = {
                'iat': datetime.utcnow(),
                'iss': 'PianoCabin',
                'openid': open_id
            }
            session = jwt.encode(payload=payload, key=CONFIGS['APP_SECRET'], algorithm='HS256')
            user = User.objects.create(open_id=open_id, session=session)
            if user is None:
                raise MsgError(msg='Creating user fails')
            redis_manage.session_user.set(session, user.id)


class Bind(APIView):
    # bind API

    def get(self):
        self.checkMsg('ticket', 'authorization')
        ticket = self.msg.get('ticket')
        user = self.getUserBySession()
        url = 'https://id.tsinghua.edu.cn/thuser/authapi/checkticket/{AppID}/{ticket}/{UserIpAddr}'
        url = parse.urljoin(url, CONFIGS['THU_APP_ID'])
        url = parse.urljoin(url, ticket)
        url = parse.urljoin(url, CONFIGS['DOMAIN'].replace('.', '_'))
        res = requests.get(url=url)
        try:
            info = json.loads(res.text)
            if info.get('code') != 0:
                raise MsgError
            else:
                user.identity = info.get('zjh')
                if info.get('yhlb') in ['J0000', 'H0000', 'J0054']:
                    user.permission = 1
                elif info.get('yhlb') in ['X0011', 'X0021', 'X0031']:
                    user.permission = 2
                user.save()
        except:
            raise MsgError('Invalid ticket')


class OrderList(APIView):
    # order/list API

    def get(self):
        self.checkMsg('authorization')
        user = self.getUserBySession()
        order_list = user.order_set.all()
        data = []
        for order in order_list:
            data.append({
                "piano_type": order.piano_room.piano_type,
                "room_num": order.piano_room.room_num,
                "start_time": order.start_time.timestamp(),
                "end_time": order.end_time.timestamp(),
                "price": order.price,
                "order_status": order.order_status,
                'create_time': order.create_time.timestamp()
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
            if feedback is None:
                raise MsgError
        except:
            raise MsgError(msg='Submitting feedback fails')


class PianoRoomList(APIView):
    # piano-rooms-list API

    def post(self):
        self.checkMsg('date', 'type', 'authorization')
        user = self.getUserBySession()
        if self.msg.get('brand'):
            rooms = PianoRoom.objects.filter(brand=self.msg.get('brand'), piano_type=self.msg.get('type'))
        else:
            rooms = PianoRoom.objects.filter(piano_type=self.msg.get('type'))

        day = (datetime.fromtimestamp(self.msg.get('date')).date() - datetime.now().date()).days
        sum_times = []
        if day >= CONFIGS['MAX_ORDER_DAYS'] or day < 0:
            raise MsgError(msg='Illegal date')
        orders_rooms = {}
        for room in rooms:
            orders_rooms[room.room_num] = json.loads(redis_manage.order_list.lindex(room.room_num, day))

        if self.msg.get('start_time') and self.msg.get('end_time'):
            start_time = self.msg.get('start_time')
            end_time = self.msg.get('end_time')
            for orders in orders_rooms.values():
                sum_time = 0
                for i in range(len(orders) - 1):
                    if orders[i + 1][0] < start_time:
                        continue
                    if orders[i][1] > end_time:
                        break
                    sum_time += min(orders[i + 1][0], end_time) - max(orders[i][1], start_time)
                sum_times.append(sum_time)
            room_time = zip(sum_times, rooms)
            room_time = sorted(room_time, reverse=True)
            sum_times, rooms = zip(*room_time)
            for i, sum_time in enumerate(sum_times):
                if sum_time < 3600:
                    rooms[i] = None

        data = []
        for room in rooms:
            if room:
                data.append({
                    'piano_type': room.piano_type,
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
        id = 0
        try:
            with transaction.atomic():
                piano_room = PianoRoom.objects.select_for_update().get(room_num=self.msg.get('room_num'))
                order = Order.objects.select_for_update().create(
                    piano_room=piano_room,
                    user=user,
                    date=datetime.fromtimestamp(self.msg.get('start_time')).date(),
                    start_time=datetime.fromtimestamp(self.msg.get('start_time')),
                    end_time=datetime.fromtimestamp(self.msg.get('end_time')),
                    create_time=datetime.now(),
                    price=self.msg.get('price'),
                )
                day = (order.date - datetime.now().date()).days
                if day >= CONFIGS['MAX_ORDER_DAYS'] or day < 0:
                    raise django.db.IntegrityError
                if redis_manage.redis_lock.acquire():
                    orders = json.loads(redis_manage.order_list.lindex(piano_room.room_num, day).decode())
                    for i in range(len(orders) + 1):
                        if i == len(orders):
                            orders.append([order.start_time.timestamp(), order.end_time.timestamp()])
                            break
                        if order.end_time.timestamp() < orders[i][0]:
                            if i > 0:
                                if order.start_time.timestamp() < orders[i - 1][1]:
                                    redis_manage.redis_lock.release()
                                    raise django.db.IntegrityError
                            orders.insert(i, [order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                            break
                    orders = json.dumps(orders)
                    redis_manage.order_list.lset(piano_room.room_num, day, orders)
                    redis_manage.unpaid_orders.set(order.id, order.create_time.timestamp())
                    redis_manage.redis_lock.release()
                id = order.id
        except django.db.IntegrityError:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='Unable to order')
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
        self.checkMsg('room_num', 'start_time', 'end_time', 'price', 'order_id', 'authorization')
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(id=self.msg.get('order_id'))
                order.piano_room = PianoRoom.objects.select_for_update().get(room_num=self.msg.get('room_num'))
                order.start_time = datetime.fromtimestamp(self.msg.get('start_time'))
                order.end_time = datetime.fromtimestamp(self.msg.get('end_time'))
                order.price = datetime.fromtimestamp(self.msg.get('price'))
                order.save()
                if redis_manage.redis_lock.acquire():
                    day = (order.date - datetime.now().date()).days
                    room_orders = json.loads(redis_manage.order_list.lindex(order.piano_room.room_num, day).decode())
                    for room_order in room_orders:
                        if room_order[2] == order.id:
                            room_order[0] = order.start_time.timestamp()
                            room_order[1] = order.end_time.timestamp()
                    room_orders = json.dumps(room_orders)
                    redis_manage.order_list.lset(order.piano_room.room_num, day, room_orders)
                    redis_manage.redis_lock.release()
        except:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='Unable to change order')


class OrderCancel(APIView):
    # order/cancel API

    def post(self):
        self.checkMsg('order_id', 'authorization')
        try:
            with transaction.atomic():
                order = Order.objects.select_for_update().get(id=self.msg.get('order_id'))
                order.order_status = 0
                order.save()
                if redis_manage.redis_lock.acquire():
                    day = (order.date - datetime.now().date()).days
                    room_orders = json.loads(redis_manage.order_list.lindex(order.piano_room.room_num, day).decode())
                    for room_order in room_orders:
                        if room_order[2] == order.id:
                            room_orders.remove(room_order)
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
            raise MsgError(msg='Unable to cancel order')

