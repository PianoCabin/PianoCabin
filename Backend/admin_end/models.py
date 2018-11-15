from django.db import models
from Backend.settings import *
import redis


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
    prices = models.TextField(default='{"student":-1,"teacher":-1,"other":-1}')
    usable = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class User(models.Model):
    open_id = models.CharField(default="", max_length=255, unique=True)
    identity = models.CharField(default="", max_length=255, unique=True, null=True, blank=True)
    permission = models.IntegerField(default=0)

    def __str__(self):
        return self.id


class Order(models.Model):
    piano_room = models.ForeignKey(PianoRoom, on_delete=models.CASCADE, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    date = models.DateField(default='2018-01-01')
    start_time = models.DateTimeField(default='2018-01-01')
    end_time = models.DateTimeField(default='2018-01-01')
    price = models.IntegerField(default=0)
    payment_status = models.IntegerField(default=1)
    order_status = models.IntegerField(default=1)

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
    is_valid = models.BooleanField(default=False)
    payment_status = models.IntegerField(default=1)
    order_status = models.IntegerField(default=1)

    def __str__(self):
        return self.id


class News(models.Model):
    title = models.TextField(default='')
    content = models.TextField(default='')
    publish_time = models.DateTimeField(default='2018-01-01')

    def __str__(self):
        return self.id


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    title = models.TextField(default='')
    content = models.TextField(default='')
    feedback_time = models.DateTimeField(default='2018-01-01')

    def __str__(self):
        return self.id


room_list = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=0)

unpaid_orders = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=1)

session_user = redis.Redis(host=CONFIGS['REDIS_HOST'], port=CONFIGS['REDIS_PORT'], db=2)
