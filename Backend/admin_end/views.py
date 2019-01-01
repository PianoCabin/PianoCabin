import datetime
import json
import traceback
from collections import defaultdict

from django.contrib import auth
from django.db import transaction
from django.db.models import Q
from django.utils import timezone

from utils.utils import *
from .models import *

# Create your views here.

try:
    redis_manage.initDatabase()
    TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'
    if not TESTING:
        time_scheduler = TimeScheduler()
        time_scheduler.scheduledUpdate()
except:
    pass


class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')

    def post(self):
        self.checkMsg("username", "password")
        user = auth.authenticate(request=self.request, username=self.msg["username"], password=self.msg["password"])
        if not user:
            raise MsgError(0, 'login failed')
        auth.login(self.request, user)


class Logout(APIView):
    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'logout failed')
        auth.logout(self.request)


class PianoRoomCreate(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num", "piano_type", "brand", "price_0", "price_1", "price_2", "usable", "art_ensemble")
        try:
            with transaction.atomic():
                new_piano_room = PianoRoom.objects.create(
                    room_num=self.msg["room_num"],
                    piano_type=self.msg["piano_type"],
                    brand=self.msg["brand"],
                    price_0=self.msg["price_0"],
                    price_1=self.msg["price_1"],
                    price_2=self.msg["price_2"],
                    usable=self.msg["usable"],
                    art_ensemble=self.msg["art_ensemble"],
                )
                if redis_manage.redis_lock.acquire():
                    for i in range(CONFIGS['MAX_ORDER_DAYS']):
                        redis_manage.order_list.rpush(new_piano_room.room_num, '[]')
                    redis_manage.redis_lock.release()
                if not new_piano_room:
                    raise MsgError(0, 'piano room create failed')
        except:
            try:
                redis_manage.redis_lock.release()
            except:
                pass
            raise MsgError(msg='piano room create failed')


class PianoRoomEdit(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num", "brand", "piano_type", "price_0", "price_1", "price_2", "usable", "art_ensemble")
        room = PianoRoom.objects.filter(room_num=self.msg['room_num'])
        if not self.msg["usable"] and room[0].usable:
            try:
                with transaction.atomic():
                    orders = Order.objects.select_for_update().filter(piano_room=room[0], order_status=1)
                    for order in orders:
                        order.order_status = 0
                        order.cancel_reason = 3
                        order.save()
                        if redis_manage.redis_lock.acquire():
                            day = (order.date - datetime.datetime.now().date()).days
                            room_orders = json.loads(
                                redis_manage.order_list.lindex(order.piano_room.room_num, day).decode())
                            length = len(room_orders)
                            for i in range(length):
                                if order.id == room_orders[i][2]:
                                    room_orders.pop(i)
                                    break
                            room_orders = json.dumps(room_orders)
                            redis_manage.order_list.lset(order.piano_room.room_num, day, room_orders)
                            redis_manage.unpaid_orders.delete(order.id)
                            redis_manage.redis_lock.release()

                # 推送信息给已支付订单
                paid_orders = Order.objects.filter(piano_room=room[0], order_status=2)
                for paid_order in paid_orders:
                    self.sendAlert(send_data={
                        "touser": paid_order.user.open_id,
                        "template_id": "uuVrW3jb2WN4MRo4DajIxX-DPyP5rNggDp3FFyBoGqk",
                        "form_id": paid_order.prepay_id,
                        "data": {
                            "keyword1": {
                                "value": "您预约的琴房被管理员下线，请联系管理员退款"
                            },
                            "keyword2": {
                                "value": paid_order.order_id
                            },
                            "keyword3": {
                                "value": paid_order.piano_room.room_num
                            },
                            "keyword4": {
                                "value": str(paid_order.price) + '元'
                            },
                            "keyword5": {
                                "value": paid_order.start_time.strftime('%Y-%m-%d %X')
                            },
                            "keyword6": {
                                "value": paid_order.end_time.strftime('%Y-%m-%d %X')
                            }
                        }
                    })
            except:
                try:
                    redis_manage.redis_lock.release()
                except:
                    pass
                raise MsgError(msg='Unable to cancel order')

        if not room.update(
                brand=self.msg["brand"],
                piano_type=self.msg["piano_type"],
                price_0=self.msg["price_0"],
                price_1=self.msg["price_1"],
                price_2=self.msg["price_2"],
                usable=self.msg["usable"],
                art_ensemble=self.msg["art_ensemble"]
        ):
            raise MsgError(0, 'fail to edit a piano room')


class PianoRoomDelete(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num")
        if not PianoRoom.objects.filter(room_num=self.msg['room_num']).update(usable=False):
            raise MsgError(0, 'fail to delete a not-exist piano room')


class PianoRoomList(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        try:
            query_str = ''
            if "piano_type" in self.msg:
                query_str += 'Q(piano_type=self.msg["piano_type"])&'
            if "room_num" in self.msg:
                query_str += 'Q(room_num=self.msg["room_num"])&'
            temp = PianoRoom.objects.filter(eval(query_str[:-1])).values(
                'brand', 'room_num', 'piano_type', 'price_0', 'price_1', 'price_2', 'usable', 'art_ensemble')
            temp = list(temp)
            dd = defaultdict(list)
            for item in temp:
                dd[item['brand']].append(item)
            return {'room_list': dd}
        except:
            raise MsgError(0, 'fail to list piano room as no such piano type exist')


class OrderList(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        count = self.checkMsgMultiOption("order_status", "identity", "start_date", "end_date", "order_id", "room_num",
                                         "user_id")
        try:
            if count:
                query_str = ''
                if "room_num" in self.msg:
                    query_str += 'Q(piano_room=get_or_none(PianoRoom, room_num=self.msg["room_num"]))&'
                if "order_id" in self.msg:
                    query_str += 'Q(order_id=self.msg["order_id"])&'
                if "identity" in self.msg:
                    query_str += 'Q(user=get_or_none(User, identity=self.msg["identity"]))&'
                if "user_id" in self.msg:
                    query_str += 'Q(user=get_or_none(User, user_id=self.msg["user_id"]))&'
                if "order_status" in self.msg:
                    query_str += 'Q(order_status=self.msg["order_status"])&'
                if "start_date" in self.msg and "end_date" in self.msg:
                    query_str += 'Q(create_time__range=[datetime.datetime.fromtimestamp(self.msg["start_date"]), datetime.datetime.fromtimestamp(self.msg["end_date"])])&'
                temp = Order.objects.filter(eval(query_str[:-1])).values(
                    'piano_room__brand', 'piano_room__room_num', 'user_id', 'start_time', 'end_time', 'price',
                    'order_id',
                    'create_time', 'order_status')
            else:
                temp = Order.objects.all().values(
                    'piano_room__brand', 'piano_room__room_num', 'user_id', 'start_time', 'end_time', 'price',
                    'order_id',
                    'create_time', 'order_status')
            temp = list(temp)
            for item in temp:
                user = User.objects.get(id=item['user_id'])
                if user.identity:
                    item['user_id'] = user.identity
                else:
                    item['user_id'] = user.user_id
                item['start_time'] = item['start_time'].timestamp()
                item['end_time'] = item['end_time'].timestamp()
                item['create_time'] = item['create_time'].timestamp()
                item['brand'] = item['piano_room__brand']
                item['room_num'] = item['piano_room__room_num']
            return {'order_list': temp}
        except:
            traceback.print_exc()
            raise MsgError(0, 'fail to list order list')


class NewsList(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        try:
            news_list = News.objects.all().values('news_title', 'id', 'publish_time')
            temp = list(news_list)
            for item in temp:
                item['publish_time'] = item['publish_time'].timestamp()
                item['news_id'] = item["id"]
            return {'news_list': temp}
        except:
            raise MsgError(0, 'fail to list news')


class NewsCreate(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_title", "news_content")
        new_news = News.objects.create(
            news_title=self.msg["news_title"],
            news_content=self.msg["news_content"],
            publish_time=timezone.now()
        )
        if not new_news:
            raise MsgError(0, 'fail to create a news')


class NewsDetail(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_id")
        try:
            detail = News.objects.filter(id=self.msg["news_id"]).values('news_title', 'news_content', 'publish_time')
            a = (list(detail))[0]
            # json无法序列化datetime
            a['publish_time'] = a['publish_time'].timestamp()
            return a
        except:
            raise MsgError(0, 'news does not exist')


class NewsDelete(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_id")
        try:
            News.objects.get(id=self.msg["news_id"]).delete()
        except:
            raise MsgError(0, 'fail to delete a news')


class FeedbackList(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        try:
            if self.msg.get('read_status'):
                temp = Feedback.objects.filter(read_status=self.msg['read_status']).values(
                    'feedback_title', 'id', 'user', 'feedback_time', 'read_status', 'feedback_content')
                a = list(temp)
                for i in a:
                    i['feedback_time'] = i['feedback_time'].timestamp()
                    i['feedback_id'] = i['id']
                    user = User.objects.get(id=i['user'])
                    if user.identity:
                        i["user_id"] = user.identity
                    else:
                        i["user_id"] = user.user_id
                return {'feedback_list': a}
            else:
                temp = Feedback.objects.all().values(
                    'feedback_title', 'id', 'user', 'feedback_time', 'read_status', 'feedback_content')
                a = list(temp)
                for i in a:
                    i['feedback_time'] = i['feedback_time'].timestamp()
                    i['feedback_id'] = i['id']
                    user = User.objects.get(id=i['user'])
                    if user.identity:
                        i["user_id"] = user.identity
                    else:
                        i["user_id"] = user.user_id
                return {'feedback_list': a}
        except:
            raise MsgError(0, 'fail to list feedback')


class FeedbackDetail(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("feedback_id")
        try:
            temp = Feedback.objects.filter(id=self.msg['feedback_id']).values(
                'feedback_title', 'feedback_content', 'id', 'user', 'feedback_time', 'read_status')[0]
            feedback = Feedback.objects.get(pk=self.msg['feedback_id'])
            feedback.read_status = 1
            feedback.save()
            user = User.objects.get(pk=temp['user'])
            a = {'feedback_content': temp['feedback_content'], 'feedback_title': temp['feedback_title'],
                 'feedback_time': temp['feedback_time'].timestamp()}
            if user.identity:
                a["user_id"] = user.identity
            else:
                a["user_id"] = user.user_id
            return a
        except:
            raise MsgError(0, 'cannot get the detail of this feedback')


class UserUpdate(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        pass


class UserList(APIView):
    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        options = self.getMultiOption('user_id', 'identity', 'permission', 'order_permission')
        users = User.objects.filter(**options).values('user_id', 'identity', 'permission', 'order_permission')
        users = list(users)
        return {'user_list': users}


class UserEdit(APIView):
    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg('user_list')
        for user_info in self.msg['user_list']:
            user = User.objects.get(user_id=user_info['user_id'])
            user.order_permission = user_info['order_permission']
            user.save()
