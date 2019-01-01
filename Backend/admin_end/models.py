import threading
from datetime import datetime, timedelta

import redis
from django.db import models

from Backend.settings import *


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
    prepay_id = models.TextField(default='')

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
    """
    redis 数据库管理类
    """

    def __init__(self):
        self.order_list = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=0)
        self.unpaid_orders = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=1)
        self.session_user = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=2)
        self.redis_lock = threading.Lock()
        # self.initDatabase()

    def initDatabase(self):
        """
        初始化redis数据库
        :return: None
        """
        self.order_list.flushdb()
        self.unpaid_orders.flushdb()
        self.session_user.flushdb()
        self.initOrderList()
        self.initUnpaidOrders()
        self.initSessionUser()

    def initOrderList(self):
        """
        初始化订单表
        :return: None
        """
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
        """
        初始化未支付订单表
        :return: None
        """
        orders = Order.objects.filter(order_status=1)
        for order in orders:
            self.unpaid_orders.rpush(order.id, order.create_time.timestamp())
            self.unpaid_orders.rpush(order.id, order.start_time.timestamp())

    def initSessionUser(self):
        """
        初始化用户-session表
        :return: None
        """
        users = User.objects.all()
        for user in users:
            self.session_user.set(user.session, user.id)


redis_manage = RedisManage()
