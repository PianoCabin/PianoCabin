from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import *
from django.utils import timezone
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
    @classmethod
    def setUpTestData(cls):
        cls.news1 = News.objects.create(
            news_title='测试标题1',
            news_content='测试内容1',
            publish_time='2018-12-08 11:00:49.834183'
        )
        cls.news2 = News.objects.create(
            news_title='测试标题2',
            news_content='测试内容2',
            publish_time='2018-12-09 11:00:49.834183'
        )

    def test_get(self):
        response = self.login_client.get('/a/news/list/')
        self.assertEqual(response.json()['code'], 1)


class NewsCreateTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.news_dict_correct = {
            'news_title': '测试标题3',
            'news_content': '测试内容3'
        }
        cls.news_dict_attribute_miss = {
            'news_title': '测试标题_wrong'
        }

    def test_post(self):
        response = self.login_client.post('/a/news/create/', self.news_dict_correct)
        self.assertEqual(response.json()['code'], 1)
        response = self.login_client.post('/a/news/create/', self.news_dict_attribute_miss)
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'API requires field "news_content"')



class NewsDetailTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.news1 = News.objects.create(
            news_title='测试标题4',
            news_content='测试内容4',
            publish_time='2018-12-10 11:00:49.834183'
        )
        cls.answer = {'news_title': '测试标题1', 'news_content': '测试内容1', 'publish_time': 1544238049.834183}

    def test_get(self):
        response = self.login_client.get('/a/news/detail/', {'news_id': 4})
        self.assertEqual(response.json()['code'], 1)
        response = self.login_client.get('/a/news/detail/', {'news_id': 100})
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'news does not exist')


class NewsDeleteTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.news1 = News.objects.create(
            news_title='测试标题5',
            news_content='测试内容5',
            publish_time='2018-12-11 11:00:49.834183'
        )
        cls.news2 = News.objects.create(
            news_title='测试标题6',
            news_content='测试内容6',
            publish_time='2018-12-12 11:00:49.834183'
        )
        cls.old_answer = {'news_list': [{'news_title': '测试标题5', 'id': 2, 'publish_time': 1544497249.834183,
                                         'news_id': 2},
                                        {'news_title': '测试标题6', 'id': 3, 'publish_time': 1544583649.834183,
                                         'news_id': 3}]}
        cls.new_answer = {'news_list': [{'news_title': '测试标题6', 'id': 3, 'publish_time': 1544583649.834183,
                                         'news_id': 3}]}

    def test_get(self):
        response = self.login_client.get('/a/news/list/')
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.old_answer)
        # 删除存在的新闻
        response = self.login_client.get('/a/news/delete/', {'news_id': 2})
        self.assertEqual(response.json()['code'], 1)
        # 删除不存在的新闻
        response = self.login_client.get('/a/news/delete/', {'news_id': 4})
        self.assertEqual(response.json()['code'], 0)
        response = self.login_client.get('/a/news/list/')
        self.assertEqual(response.json()['data'], self.new_answer)


class FeedbackListTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            open_id='123456789',
            identity='123456789',
            permission=0,
            session='123456789'
        )
        cls.feedback_1 = Feedback.objects.create(
            user=cls.user1,
            feedback_title='反馈标题1',
            feedback_content='反馈内容1',
            read_status=False,
            feedback_time='2018-12-10'
        )
        cls.feedback_2 = Feedback.objects.create(
            user=cls.user1,
            feedback_title='反馈标题2',
            feedback_content='反馈内容2',
            read_status=True,
            feedback_time='2018-12-10'
        )
        cls.answer_1 = {'feedback_list': [{'feedback_title': '反馈标题1', 'id': 3, 'user': 2,
                                           'feedback_time': 1544371200.0, 'read_status': False,
                                           'feedback_content': '反馈内容1', 'feedback_id': 3, 'user_id': '123456789'}]}
        cls.answer_2 = {'feedback_list': [{'feedback_title': '反馈标题2', 'id': 4, 'user': 2,
                                           'feedback_time': 1544371200.0, 'read_status': True,
                                           'feedback_content': '反馈内容2', 'feedback_id': 4, 'user_id': '123456789'}]}

    def test_get(self):
        # 请求未读信息
        response = self.login_client.get('/a/feedback/list/', {'read_status': 0})
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_1)
        # 请求已读信息
        response = self.login_client.get('/a/feedback/list/', {'read_status': 1})
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_2)


class FeedbackDetailTest(MyTest):
    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(
            open_id='1234567890',
            identity='1234567890',
            permission=0,
            session='1234567890'
        )
        cls.feedback_1 = Feedback.objects.create(
            user=cls.user1,
            feedback_title='反馈标题3',
            feedback_content='反馈内容3',
            read_status=False,
            feedback_time='2018-12-10'
        )
        cls.feedback_2 = Feedback.objects.create(
            user=cls.user1,
            feedback_title='反馈标题4',
            feedback_content='反馈内容4',
            read_status=True,
            feedback_time='2018-12-10'
        )
        cls.answer_1 = {'feedback_content': '反馈内容3', 'feedback_title': '反馈标题3', 'feedback_time': 1544371200.0,
                        'user_id': '1234567890'}

    def test_get(self):
        response = self.login_client.get('/a/feedback/detail/', {'feedback_id': 1})
        self.assertEqual(response.json()['code'], 1)
        self.assertEqual(response.json()['data'], self.answer_1)
        response = self.login_client.get('/a/feedback/detail/', {'feedback_id': 100})
        self.assertEqual(response.json()['code'], 0)
        self.assertEqual(response.json()['msg'], 'cannot get the detail of this feedback')


class UserUpdateTest(MyTest):
    pass
