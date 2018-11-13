from django.db import models
from datetime import datetime


# Create your models here.
def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


class PianoRoom(models.Model):
    room_num = models.TextField(default='')
    piano_type = models.TextField(default='')
    brand = models.TextField(default='')
    prices = models.TextField(default='{"student":-1,"teacher":-1,"other":-1}')
    usable = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class User(models.Model):
    open_id = models.TextField(default="")
    identity = models.TextField(default="")
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
