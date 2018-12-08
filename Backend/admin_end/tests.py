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
        cls.login_client = Client()
        cls.login_client.login(username=cls.username, password=cls.password)
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
        cls.temp_room = PianoRoom.objects.create(
            room_num='F2-202',
            piano_type='电钢琴',
            brand='杂牌',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )
        cls.piano_room_msg_dict_edit = {
            'room_num': 'F2-202',
            'piano_type': '电子琴',
            'brand': '新牌',
            'price_0': 100,
            'price_1': 80,
            'price_2': 60,
            'usable': False,
            'art_ensemble': 1
        }

    def test_post(self):
        response = self.login_client.post('/a/piano-room/edit/', self.piano_room_msg_dict_edit)
        self.assertEqual(response.json()['code'], 1)


class PianoRoomDeleteTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.temp_room = PianoRoom.objects.create(
            room_num='F2-202',
            piano_type='电钢琴',
            brand='杂牌',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )
        cls.piano_room_msg_dict_delete_correct = {
            'room_num': 'F2-202',
        }
        cls.piano_room_msg_dict_delete_fault = {
            'room_num': 'F2-201',
        }

    def test_post(self):
        response = self.login_client.post('/a/piano-room/delete/', self.piano_room_msg_dict_delete_correct)
        self.assertEqual(response.json()['code'], 1)
        response = self.login_client.post('/a/piano-room/delete/', self.piano_room_msg_dict_delete_fault)
        self.assertEqual(response.json()['code'], 0)


class PianoRoomListTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        # piano_type room_num 可组合选择
        cls.temp_room_1 = PianoRoom.objects.create(
            room_num='F2-202',
            piano_type='电子琴',
            brand='A',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )
        cls.temp_room_2 = PianoRoom.objects.create(
            room_num='F2-203',
            piano_type='钢琴',
            brand='B',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )
        cls.temp_room_3 = PianoRoom.objects.create(
            room_num='F2-204',
            piano_type='钢琴',
            brand='B',
            price_0=10,
            price_1=8,
            price_2=6,
            usable=1,
            art_ensemble=0
        )
        cls.query_dict_1 = {'room_num': 'F2-202', 'piano_type': '电子琴'}
        cls.query_dict_2 = {'room_num': 'F2-202', 'piano_type': '钢琴'}
        cls.query_dict_3 = {'piano_type': '钢琴'}
        cls.query_dict_4 = {'piano_type': '小提琴'}
        cls.query_dict_5 = {'room_num': 'F2-204'}
        cls.query_dict_6 = {}
        cls.answer_1 = {'room_list': {'A': [{'brand': 'A', 'room_num': 'F2-202', 'piano_type': '电子琴', 'price_0': 10,
                                             'price_1': 8, 'price_2': 6, 'usable': True, 'art_ensemble': 0}]}}
        cls.answer_2 = {'room_list': {}}
        cls.answer_3 = {'room_list': {'B': [{'brand': 'B', 'room_num': 'F2-203', 'piano_type': '钢琴', 'price_0': 10,
                                             'price_1': 8, 'price_2': 6, 'usable': True, 'art_ensemble': 0},
                                            {'brand': 'B', 'room_num': 'F2-204', 'piano_type': '钢琴', 'price_0': 10,
                                             'price_1': 8, 'price_2': 6, 'usable': True, 'art_ensemble': 0}]}}
        cls.answer_4 = {'room_list': {}}
        cls.answer_5 = {'room_list': {'B': [{'brand': 'B', 'room_num': 'F2-204', 'piano_type': '钢琴', 'price_0': 10,
                                             'price_1': 8, 'price_2': 6, 'usable': True, 'art_ensemble': 0}]}}
        cls.answer_6 = None

    def test_post(self):
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_1)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_1)
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_2)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_2)
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_3)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_3)
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_4)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_4)
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_5)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_5)
        response = self.login_client.post('/a/piano-room/list/', self.query_dict_6)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'fail to list piano room as no such piano type exist')
        self.assertEqual(response.json()['data'], self.answer_6)


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
