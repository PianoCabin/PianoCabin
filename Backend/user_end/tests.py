from django.test import TestCase, Client
from admin_end.models import *
from utils.utils import *
from datetime import datetime, timedelta
import json


# Create your tests here.
class LoginTest(TestCase):

    # 测试Login API
    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 测试错误code
        response = self.client.post('/u/login/', {
            'code': '0333HhU02scqeZ0wYIX02RIpU023HhUB'
        })
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)

        # 测试无code
        response = self.client.post('/u/login/', None)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)


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

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 正确输入1
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 15, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        # 正确输入2
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime.now() + timedelta(days=1)).timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 15, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        # 正确输入3(绑定用户)
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime.now() + timedelta(days=1)).timestamp(),
            'type': '钢琴房',
            'authorization': self.user_2.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user_2.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 10, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 10, 'occupied_time': []}]
        }, response.json()['data'])

        # 不存在用户
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION='test')

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)

        # 不存在用户(无请求头)
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json')

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)

        # 不存在琴房类型
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': 'test',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual(response.json()['data'], {'room_list': []})

        # 提交日期不正确
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime.now() - timedelta(days=1)).timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)

        # 提交日期不正确
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime.now() + timedelta(days=CONFIGS['MAX_ORDER_DAYS'])).timestamp(),
            'type': '钢琴房',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)

        # 测试搜索品牌
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'brand': '星海立式钢琴',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': [
            {'brand': '星海立式钢琴', 'room_num': 'F2-203', 'unit_price': 15, 'occupied_time': []},
            {'brand': '星海立式钢琴', 'room_num': 'F2-205', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        # 测试搜索品牌
        self.room_3.usable = True
        self.room_3.save()

        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'brand': '卡瓦伊立式钢琴',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': [
            {'brand': '卡瓦伊立式钢琴', 'room_num': 'F2-207', 'unit_price': 15, 'occupied_time': []}]
        }, response.json()['data'])

        self.room_3.usable = False
        self.room_3.save()

        # 测试搜索品牌
        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': datetime.now().timestamp(),
            'type': '钢琴房',
            'brand': '卡瓦伊立式钢琴',
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertDictEqual({'room_list': []}, response.json()['data'])

        # 测试搜索时间
        now = datetime.now()
        self.client.post('/u/order/normal/', {
            'room_num': 'F2-205',
            'start_time': (datetime(now.year, now.month, now.day, 12) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 14) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime(now.year, now.month, now.day) + timedelta(days=1)).timestamp(),
            'type': '钢琴房',
            'start_time': (datetime(now.year, now.month, now.day, 12) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(len(response.json()['data']['room_list']), 1)
        self.assertEqual(response.json()['data']['room_list'][0]['room_num'], 'F2-203')

        # 测试搜索时间
        now = datetime.now()
        self.client.post('/u/order/normal/', {
            'room_num': 'F2-205',
            'start_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 13, 20) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 12) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        response = self.client.post('/u/order/piano-rooms-list/', {
            'date': (datetime(now.year, now.month, now.day) + timedelta(days=1)).timestamp(),
            'type': '钢琴房',
            'start_time': (datetime(now.year, now.month, now.day, 12) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'authorization': self.user.session
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(len(response.json()['data']['room_list']), 2)
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

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        now = datetime.now()
        # 正确预约1
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(Order.objects.get(order_id=response.json()['data']['order_id']).piano_room.room_num, 'F2-203')
        self.assertEqual(Order.objects.get(order_id=response.json()['data']['order_id']).price, 15)

        # 正确预约2
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 14) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(Order.objects.get(order_id=response.json()['data']['order_id']).piano_room.room_num, 'F2-203')
        self.assertEqual(Order.objects.get(order_id=response.json()['data']['order_id']).price, 15)

        # 错误房间号
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-200',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 无房间号
        response = self.client.post('/u/order/normal/', {
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误价格
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 10,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误价格
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': '10',
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 无价格
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误时间（重复预约）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误时间（部分重复预约）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15, 20).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误时间（在开放时间之前或关门时间之后）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day, 9).timestamp(),
            'end_time': datetime(now.year, now.month, now.day, 10).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 0) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误时间（开始结束不在同一天）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 15, 20).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 2, 16, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 错误时间（开始晚于结束）
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 2, 15, 20).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 16, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        # 无时间
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 无开始时间
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'end_time': datetime(now.year, now.month, now.day + 1, 16, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)

        # 无结束时间
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': datetime(now.year, now.month, now.day + 1, 16, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)
        self.assertEqual(len(Order.objects.all()), 2)


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

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()
        now = datetime.now()
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 19) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 20) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.order_id = response.json()['data']['order_id']

    def test_post(self):
        now = datetime.now()
        # 正确提交1
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        # 正确提交2
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 13) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 14) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        # 正确提交3（不变）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        # 错误id
        response = self.client.post('/u/order/change/', {
            'order_id': 'test',
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无id
        response = self.client.post('/u/order/change/', {
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误价格
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'price': 10,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误价格
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'price': '10',
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无价格
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（重复预约）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 18) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 20) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（部分重复预约）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': datetime(now.year, now.month, now.day + 1, 18, 20).timestamp(),
            'end_time': datetime(now.year, now.month, now.day + 1, 20, 20).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误时间（在开放时间之前或关门时间之后）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 9).timestamp(),
            'end_time': datetime(now.year, now.month, now.day, 10).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': (datetime(now.year, now.month, now.day, 17) + timedelta(days=1)).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 0) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误日期
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day, 17).timestamp(),
            'start_time': datetime(now.year, now.month, now.day, 23).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 0) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误日期（超出预约最长日期）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day, 17).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'])).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'])).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 错误日期（开始结束不在同一日期）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day, 17).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'])).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        # 错误时间（开始晚于结束）
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'date': datetime(now.year, now.month, now.day, 17).timestamp(),
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 2)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无日期
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 2)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无时间
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无开始时间
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 2)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无结束时间
        response = self.client.post('/u/order/change/', {
            'order_id': self.order_id,
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 17) + timedelta(
                days=CONFIGS['MAX_ORDER_DAYS'] - 2)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)


class OrderCancelTest(TestCase):

    # 测试OrderCancel API
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

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()
        now = datetime.now()
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 19) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 20) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.order_id = response.json()['data']['order_id']

    def test_post(self):
        # 正确取消
        response = self.client.post('/u/order/cancel/', {
            'order_id': self.order_id
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        self.assertEqual(get_or_none(Order, order_id=self.order_id).order_status, 0)
        self.assertEqual(get_or_none(Order, order_id=self.order_id).cancel_reason, 2)

        # id错误
        response = self.client.post('/u/order/cancel/', {
            'order_id': 'test'
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        self.assertEqual(get_or_none(Order, order_id=self.order_id).order_status, 0)

        # 无id
        response = self.client.post('/u/order/cancel/', {
            'order_id': 'test'
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        self.assertEqual(get_or_none(Order, order_id=self.order_id).order_status, 0)

        # 重复取消
        response = self.client.post('/u/order/cancel/', {
            'order_id': self.order_id
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        self.assertEqual(get_or_none(Order, order_id=self.order_id).order_status, 0)

        # 取消已支付订单
        order = Order.objects.get(order_id=self.order_id)
        order.order_status = 2
        order.save()

        response = self.client.post('/u/order/cancel/', {
            'order_id': self.order_id
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        self.assertEqual(get_or_none(Order, order_id=self.order_id).order_status, 2)

        order = Order.objects.get(order_id=self.order_id)
        order.order_status = 1
        order.save()


class BindTest(TestCase):
    # 测试Bind API

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()
        self.sign = APIView.getSign({
            'identity': '12321321',
            'permission': 1,
            'name': 'aaa'
        })

    def test_post(self):
        # sign错误
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'permission': 1,
                'name': 'aaa',
                'sign': 'test'
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无sign
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'name': 'aaa',
                'permission': 1,
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 无session
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'permission': 1,
                'name': 'aaa',
                'sign': 'test'
            }
        }, content_type='application/json')

        self.assertEqual(response.json()['code'], 0)

        # 无姓名
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'permission': 1,
                'sign': self.sign
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 正确提交
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'permission': 1,
                'name': 'aaa',
                'sign': self.sign
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)

        # 已绑定用户
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '12321321',
                'permission': 1,
                'name': 'aaa',
                'sign': self.sign
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)

        # 绑定他人账号
        self.sign = APIView.getSign({
            'identity': '1321312321',
            'permission': 1,
            'name': 'aaa'})
        response = self.client.post('/u/bind/confirmed/', {
            'user_info': {
                'identity': '1321312321',
                'permission': 1,
                'name': 'aaa',
                'sign': self.sign
            }
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)


class BindInfoTest(TestCase):
    # 测试BindInfo API

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 未绑定用户
        response = self.client.get('/u/bind/info/', None, HTTP_AUTHORIZATION=self.user.session)
        self.assertDictEqual(response.json()['data'], {
            'identity': self.user.identity,
            'name': self.user.name,
            'permission': self.user.permission
        })

        # 已绑定用户
        response = self.client.get('/u/bind/info/', None, HTTP_AUTHORIZATION=self.user_2.session)
        self.assertDictEqual(response.json()['data'], {
            'identity': self.user_2.identity,
            'name': self.user_2.name,
            'permission': self.user_2.permission
        })

        # 无session
        response = self.client.get('/u/bind/info/', None)
        self.assertEqual(response.json()['code'], 0)


class CreateFeedBackTest(TestCase):
    # 测试BindInfo API

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 正确提交
        response = self.client.post('/u/feedback/', {
            'feedback_title': 'test_title',
            'feedback_content': 'test_content'
        }, HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 1)
        feedback = Feedback.objects.get(user=self.user)
        self.assertEqual(feedback.feedback_title, 'test_title')
        self.assertEqual(feedback.feedback_content, 'test_content')

        # 无标题
        response = self.client.post('/u/feedback/', {
            'feedback_content': 'test_content'
        }, HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(len(Feedback.objects.all()), 1)

        # 无内容
        response = self.client.post('/u/feedback/', {
            'feedback_title': 'test_title'
        }, HTTP_AUTHORIZATION=self.user.session)

        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(len(Feedback.objects.all()), 1)


class OrderListTest(TestCase):
    # 测试OrderList API

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

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()
        now = datetime.now()
        response = self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 15) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 16) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.client.post('/u/order/normal/', {
            'room_num': 'F2-203',
            'start_time': (datetime(now.year, now.month, now.day, 19) + timedelta(days=1)).timestamp(),
            'end_time': (datetime(now.year, now.month, now.day, 20) + timedelta(days=1)).timestamp(),
            'price': 15,
        }, content_type='application/json', HTTP_AUTHORIZATION=self.user.session)

        self.order_id = response.json()['data']['order_id']

    def test_get(self):
        # 正确提交(无order_id)
        print(len(Order.objects.all()))
        response = self.client.get('/u/order/list/', None, HTTP_AUTHORIZATION=self.user.session)
        self.assertEqual(len(response.json()['data']['order_list']), 2)
        self.assertEqual(response.json()['data']['order_list'][0]['room_num'], 'F2-203')

        # 正确提交(有order_id)
        response = self.client.get('/u/order/list/', {
            'order_id': self.order_id
        }, HTTP_AUTHORIZATION=self.user.session)
        self.assertEqual(len(response.json()['data']['order_list']), 1)
        self.assertEqual(response.json()['data']['order_list'][0]['room_num'], 'F2-203')

        # 无session
        response = self.client.get('/u/order/list/', None)
        self.assertEqual(response.json()['code'], 0)


class NewsList(TestCase):
    # 测试NewsList API

    @classmethod
    def setUpTestData(cls):
        cls.news_1 = News.objects.create(news_title='test_title_1',
                                         news_content='test_content_1',
                                         publish_time=datetime.now())

        cls.news_2 = News.objects.create(news_title='test_title_2',
                                         news_content='test_content_2',
                                         publish_time=datetime.now())

        cls.news_3 = News.objects.create(news_title='test_title_3',
                                         news_content='test_content_3',
                                         publish_time=datetime.now())

        cls.user = User.objects.create(
            open_id='xxxxxxxxxxxxxxxxx',
            session='aaaaaaaaaaaaaaaaa'
        )

        cls.user_2 = User.objects.create(
            open_id='xxxxxxxxx',
            session='aaaaaaaaaa',
            permission=1,
            identity='1321312321'
        )

        redis_manage.initDatabase()

    def setUp(self):
        self.client = Client()

    def test_post(self):
        # 正确提交(无news_id)
        response = self.client.post('/u/news/list/', None, HTTP_AUTHORIZATION=self.user.session)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(len(response.json()['data']['news_list']), 3)
        for i in range(3):
            self.assertEqual(response.json()['data']['news_list'][i]['news_title'], 'test_title_'+str(i+1))
            self.assertEqual(response.json()['data']['news_list'] [i]['news_content'], 'test_content_' + str(i + 1))

        # 正确提交(有news_id)
        response = self.client.post('/u/news/list/', {
            'news_id': self.news_1.id
        }, HTTP_AUTHORIZATION=self.user.session)
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(len(response.json()['data']['news_list']), 1)
        self.assertEqual(response.json()['data']['news_list'][0]['news_title'], 'test_title_1')
        self.assertEqual(response.json()['data']['news_list'][0]['news_content'], 'test_content_1')

        # 无session
        response = self.client.post('/u/news/list/', {
            'news_id': self.news_1.id
        })
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['data'], None)