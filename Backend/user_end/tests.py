from django.test import TestCase, Client
from admin_end.models import *
from datetime import datetime, timedelta
import json


# Create your tests here.
class LoginTest(TestCase):

    # 测试Login API
    def setUp(self):
        self.client = Client()

    def test_post(self):
        response = self.client.post('/u/login/', {
            'code': '0333HhU02scqeZ0wYIX02RIpU023HhUB'
        })
        self.assertEqual(response.json()['code'], 0)


class PianoListTest(TestCase):

    # 测试PianoList API
    @classmethod
    def setUpTestData(cls):
        cls.room_1 = PianoRoom.objects.create(
            room_num='F2-203',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_2 = PianoRoom.objects.create(
            room_num='F2-205',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_3 = PianoRoom.objects.create(
            room_num='F2-207',
            piano_type='钢琴房',
            brand='卡瓦伊立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=False
        )

        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 正确输入
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 15, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        # 不存在用户
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION='test')

        self.assertEqual(response.json()['code'], 0)

        # 不存在琴房类型
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': 'test',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertDictEqual(response.json()['data'], {'room_list': []})

        # 提交日期不正确
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime.now() - timedelta(days=1)).timestamp(),
            'type': 'test',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 测试搜索品牌
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'brand': '星海立式钢琴',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 15, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        # 测试搜索时间
        now = datetime.now()
        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime(now.year, now.month, now.day + 1).timestamp(),
            'type': '钢琴房',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['data']['room_list'][0]['room_num'], 'F2-205')
        self.assertEqual(response.json()['data']['room_list'][1]['room_num'], 'F2-203')


class OrderNormalTest(TestCase):

    # 测试OrderNormal API
    @classmethod
    def setUpTestData(cls):
        cls.room_1 = PianoRoom.objects.create(
            room_num='F2-203',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_2 = PianoRoom.objects.create(
            room_num='F2-205',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_3 = PianoRoom.objects.create(
            room_num='F2-207',
            piano_type='钢琴房',
            brand='卡瓦伊立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=False
        )

        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        now = datetime.now()
        # 正确预约
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        # 错误房间号
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-200',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误价格
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 10,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（重复预约）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（在开放时间之前或关门时间之后）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day, 9).timestamp(),
            'end_time': datetime(now.year, now.month, now.day, 10).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 0).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)


class OrderChangeTest(TestCase):
    
    # 测试OrderChange API
    @classmethod
    def setUpTestData(cls):
        cls.room_1 = PianoRoom.objects.create(
            room_num='F2-203',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_2 = PianoRoom.objects.create(
            room_num='F2-205',
            piano_type='钢琴房',
            brand='星海立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=True
        )

        cls.room_3 = PianoRoom.objects.create(
            room_num='F2-207',
            piano_type='钢琴房',
            brand='卡瓦伊立式钢琴',
            price_0=15,
            price_1=10,
            price_2=5,
            usable=False
        )

        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()
        now = datetime.now()
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 19).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.order_id = response.json()['data']['order_id']

    def test_post(self):
        now = datetime.now()
        # 正确提交
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        
        # 错误id
        response = self.client.post('/u/order/change/', {
            'order_id': 'test',
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误价格
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'price': 10,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（重复预约）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day + 1, 18).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（在开放时间之前或关门时间之后）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 9).timestamp(),
            'end_time': datetime(now.year, now.month, now.day, 10).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day + 1, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 0).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误日期
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 0).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)