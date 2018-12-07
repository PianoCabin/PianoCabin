from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import *
import json

# Create your tests here.
DefaultUser = get_user_model()


class MyTest(TestCase):
    '''预设公用数据'''
    @classmethod
    def setUpClass(cls):
        super(MyTest, cls).setUpClass()
        cls.username = 'pianocabin'
        cls.password = 'pianocabin'
        cls.wrong_username = 'wrongusername'
        cls.wrong_password = 'wrongpassword'
        cls.user = DefaultUser.objects.create(username=cls.username)
        cls.user.set_password(cls.password)
        cls.user.save()
        cls.client = Client()
        cls.login_client = Client().login(username=cls.username, password=cls.password)
        redis_manage.initDatabase()


class LoginTest(MyTest):

    def test_get(self):
        # 初始未登录
        response = self.client.get('/a/login/')
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'not login')

    def test_post(self):
        # 错误账号登录
        response = self.client.post('/a/login/', {"username": self.wrong_username, "password": self.password})
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'login failed')
        # 错误密码登录
        response = self.client.post('/a/login/', {"username": self.username, "password": self.wrong_password})
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'login failed')
        # 正确账号密码登录
        response = self.client.post('/a/login/', {"username": self.username, "password": self.password})
        self.assertEqual(response.json()['code'], 1)
        # 登录成功后检查状态
        response = self.client.get('/a/login/')
        self.assertEqual(response.json()['code'], 1)


class LogoutTest(MyTest):

    def test_post(self):
        # 登录后logout
        self.client.post('/a/login/', {"username": self.username, "password": self.password})
        response = self.client.post('/a/logout/')
        self.assertEqual(response.json()['code'], 1)
        # 未登录就logout
        response = self.client.post('/a/logout/')
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'logout failed')


class PianoRoomCreateTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.piano_room_msg_dict_correct = {
            'room_num': 'F2-201',
            'piano_type': '电子琴',
            'brand': '杂牌',
            'price_0': 10,
            'price_1': 8,
            'price_2': 6,
            'usable': True,
            'art_ensemble': 0
        }
        cls.piano_room_msg_dict_type_fault = {
            'room_num': 'F2-201',
            'piano_type': '电子琴',
            'brand': '杂牌',
            'price_0': 10,
            'price_1': 8,
            'price_2': 6,
            'usable': True,
            'art_ensemble': 0
        }
        cls.piano_room_msg_dict_attribute_miss = {
            'room_num': 'F2-201',
            'piano_type': '电子琴',
            'brand': '杂牌',
            'price_0': 10,
            'price_1': 8,
            'price_2': 6,
            'usable': True,
        }

    def test_post(self):
        # 正确创建
        response = self.login_client.post('/a/piano-room/create/', self.piano_room_msg_dict_correct)
        self.assertEqual(response.json()['code'], 1)
        # 属性类型错误
        response = self.login_client.post('/a/piano-room/create/', self.piano_room_msg_dict_type_fault)
        self.assertEqual(response.json()['code'], 0)
        # 缺失属性
        response = self.login_client.post('/a/piano-room/create/', self.piano_room_msg_dict_attribute_miss)
        self.assertEqual(response.json()['code'], 0)


class PianoRoomEditTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        temp_room = PianoRoom.objects.create(
            room_num='F2-202',
            piano_type='电钢琴',
            brand='杂牌',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )

    def test_post(self):
        self.login_client



class PianoRoomDeleteTest(MyTest):
    pass


class PianoRoomListTest(MyTest):
    pass


class OrderListTest(MyTest):
    pass


class NewsListTest(MyTest):
    pass


class NewsCreateTest(MyTest):
    pass


class NewsDetailTest(MyTest):
    pass


class NewsDeleteTest(MyTest):
    pass


class FeedbackListTest(MyTest):
    pass


class FeedbackDetailTest(MyTest):
    pass


class UserUpdateTest(MyTest):
    pass
