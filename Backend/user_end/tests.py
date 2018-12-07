from django.test import TestCase, Client
from admin_end.models import *
from datetime import datetime, timedelta
import json


# Create your tests here.
# class LoginTest(TestCase):
#
#     # 测试Login API
#     def setUp(self):
#         self.client = Client()
#
#     def test_post(self):
#         response = self.client.post('/u/login/', {
#             'code': '0333HhU02scqeZ0wYIX02RIpU023HhUB'
#         })
#         self.assertEqual(response.json()['code'], 0)


# class PianoListTest(TestCase):
#
#     # 测试PianoList API
#     @classmethod
#     def setUpTestData(cls):
#         cls.room_1 = PianoRoom.objects.create(
#             room_num='F2-203',
#             piano_type='钢琴房',
#             brand='星海立式钢琴',
#             price_0=15,
#             price_1=10,
#             price_2=5,
#             usable=True
#         )
#
#         cls.room_2 = PianoRoom.objects.create(
#             room_num='F2-205',
#             piano_type='钢琴房',
#             brand='星海立式钢琴',
#             price_0=15,
#             price_1=10,
#             price_2=5,
#             usable=True
#         )
#
#         cls.user = User.objects.create(
#             open_id='xxxxxxxxxxxxxxxxx',
#             session='aaaaaaaaaaaaaaaaa'
#         )
#
#         redis_manage.session_user.set(cls.user.session, cls.user.id)
#
#     def setUp(self):
#         self.client = Client()
#
#     def test_post(self):
#         response = self.client.post('/u/order/piano-rooms-list/', {
#             'date': datetime.now().timestamp(),
#             'type': '钢琴房',
#             'authorization': self.user.session
#         })
#
#         print(response.json()['data'])