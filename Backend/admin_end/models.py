from django.db import models
from Backend.settings import *
from datetime import datetime, timedelta
from django.db import transaction
import redis
import threading
import json
import requests
import time


# Create your models here.
def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class PianoRoom(models.Model):
    room_num = models.CharField(default='', max_length=255, unique=True)
    piano_type = models.TextField(default='')
    brand = models.TextField(default='')
    price_0 = models.IntegerField(default=0)
    price_1 = models.IntegerField(default=0)
    price_2 = models.IntegerField(default=0)
    art_ensemble = models.IntegerField(default=0)
    usable = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class User(models.Model):
    open_id = models.CharField(default="", max_length=255, unique=True)
    user_id = models.CharField(default=None, max_length=255, unique=True, null=True, blank=True)
    identity = models.CharField(default=None, max_length=255, unique=True, null=True, blank=True)
    permission = models.IntegerField(default=0)
    session = models.TextField(default='')
    name = models.TextField(default='')
    order_permission = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class Order(models.Model):
    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, default='')
    order_id = models.CharField(default='', max_length=128, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    date = models.DateField(default='2018-01-01')
    start_time = models.DateTimeField(default='2018-01-01')
    end_time = models.DateTimeField(default='2018-01-01')
    create_time = models.DateTimeField(default='2018-01-01')
    price = models.IntegerField(default=0)
    order_status = models.IntegerField(default=1)
    cancel_reason = models.IntegerField(default=0)
    form_id = models.TextField(default='')

    def __str__(self):
        return self.id


class LongTermOrder(models.Model):
    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    start_date = models.DateField(default='2018-01-01')
    end_date = models.DateField(default='2018-01-01')
    day_in_week = models.IntegerField(default=1)
    start_time = models.DateTimeField(default='2018-01-01')
    end_time = models.DateTimeField(default='2018-01-01')
    price = models.IntegerField(default=0)
    order_status = models.IntegerField(default=1)

    def __str__(self):
        return self.id


class News(models.Model):
    news_title = models.TextField(default='')
    news_content = models.TextField(default='')
    publish_time = models.DateTimeField(default='2018-01-01')

    def __str__(self):
        return self.id


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    feedback_title = models.TextField(default='')
    feedback_content = models.TextField(default='')
    read_status = models.BooleanField(default=False)
    feedback_time = models.DateTimeField(default='2018-01-01')

    def __str__(self):
        return self.id


class RedisManage:
    # redis 数据库管理类
    def __init__(self):
        self.order_list = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=0)
        self.unpaid_orders = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=1)
        self.session_user = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=2)
        self.redis_lock = threading.Lock()
        # self.initDatabase()

    def initDatabase(self):
        self.order_list.flushdb()
        self.unpaid_orders.flushdb()
        self.session_user.flushdb()
        self.initOrderList()
        self.initUnpaidOrders()
        self.initSessionUser()

    def initOrderList(self):
        rooms = PianoRoom.objects.all()
        for room in rooms:
            for i in range(CONFIGS['MAX_ORDER_DAYS']):
                date = datetime.now().date() + timedelta(days=i)
                orders = Order.objects.filter(date=date, piano_room=room, order_status__range=[1, 2]).order_by(
                    'start_time')
                orders_data = []
                for order in orders:
                    orders_data.append([order.start_time.timestamp(), order.end_time.timestamp(), order.id])
                orders_data = json.dumps(orders_data)
                self.order_list.rpush(room.room_num, orders_data)

    def initUnpaidOrders(self):
        orders = Order.objects.filter(order_status=1)
        for order in orders:
            self.unpaid_orders.rpush(order.id, order.create_time.timestamp())
            self.unpaid_orders.rpush(order.id, order.start_time.timestamp())

    def initSessionUser(self):
        users = User.objects.all()
        for user in users:
            self.session_user.set(user.session, user.id)


redis_manage = RedisManage()


def updateOrderList():
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


def updateUnpaidOrders():
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


def imminentOrderAlert():
    ids = redis_manage.order_list.keys()
    for id in ids:
        room_orders = redis_manage.order_list.lindex(id, 0).decode()
        room_orders = json.loads(room_orders)
        for room_order in room_orders:
            if datetime.now().timestamp() - room_order[0] < CONFIGS['ALERT_TIME'] * 60:
                order = Order.objects.get(id=room_order[2])
                if order.order_status == 2 and order.form_id != '':
                    sendAlert(order)


def sendAlert(order):
    data = {
        'grant_type': 'client_credential',
        'appid': CONFIGS['APP_ID'],
        'secret': CONFIGS['APP_SECRET'],
    }
    res = requests.get(url='https://api.weixin.qq.com/cgi-bin/token', params=data).json()
    access_token = res["access_token"]

    data = {
        "touser": order.user.open_id,
        "template_id": "ki8_cVjacJyR5FsfcJCOjW-kcYMtcYkAi1vIuIktVrk",
        "form_id": order.form_id,
        "data": {
            "keyword1": {
                "value": "您预约的琴房还有"+str(CONFIGS['ALERT_TIME'])+"分钟开始"
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
    }
    res = requests.post(
        url="https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + access_token,
        data=json.dumps(data)).json()
    print(order.form_id)
    order.form_id = ''
    order.save()
    print(res)


def scheduledUpdate():
    threading.Thread(target=runSchedule).start()


def runSchedule():
    while True:
        updateUnpaidOrders()
        imminentOrderAlert()
        if datetime.now().hour == 0 and datetime.now().minute == 1:
            updateOrderList()
        time.sleep(1)
