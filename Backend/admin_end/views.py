from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.decorators import method_decorator
from utils.utils import *
from .models import *
import json


# Create your views here.


class Login(APIView):
    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')

    def post(self):
        self.checkMsg("username", "password")
        user = auth.authenticate(request=self.request, username=self.msg["username"], password=self.msg["password"])
        if not user:
            raise MsgError(0, 'login failed')
        auth.login(self.request, user)


class Logout(APIView):
    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'logout failed')
        auth.logout(self.request)


class PianoRoomCreate(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num", "piano_type", "brand", "price_0", "price_1", "price_2", "usable", "art_ensemble")
        new_piano_room = PianoRoom.objects.create(
            room_num=self.msg["room_num"],
            piano_type=self.msg["piano_type"],
            brand=self.msg["brand"],
            price_0=self.msg["price_0"],
            price_1=self.msg["price_1"],
            price_2=self.msg["price_2"],
            usable=self.msg["usable"],
            art_ensemble=self.msg["art_ensemble"],
        )
        if not new_piano_room:
            raise MsgError(0, 'piano room create failed')


class PianoRoomEdit(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num", "brand", "piano_type", "price_0", "price_1", "price_2", "usable", "art_ensemble")
        if not PianoRoom.objects.filter(room_num=self.msg['room_num']).update(
            brand=self.msg["brand"],
            piano_type=self.msg["piano_type"],
            price_0=self.msg["price_0"],
            price_1=self.msg["price_1"],
            price_2=self.msg["price_2"],
            usable=self.msg["usable"],
            art_ensemble=self.msg["art_ensemble"]
        ):
            raise MsgError(0, 'fail to edit a piano room')


class PianoRoomDelete(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("room_num")
        if not PianoRoom.objects.filter(room_num=self.msg['room_num']).update(usable=False):
            raise MsgError(0, 'fail to delete a not-exist piano room')


class PianoRoomList(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("piano_type")
        try:
            temp = PianoRoom.objects.filter(piano_type=self.msg['piano_type']).values(
                    'room_num', 'usable')
            return json.dumps({'room_list': json.dumps(list(temp))})
        except:
            raise MsgError(0, 'fail to list piano room as no such piano type exist')


class OrderList(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        pass


class NewsList(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        try:
            news_list = News.objects.all().values('news_title', 'id', 'publish_time')
            return json.dumps({'news_list': json.dumps(list(news_list))})
        except:
            raise MsgError(0, 'fail to list news')


class NewsCreate(APIView):

    def post(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_title", "news_content")
        new_news = News.objects.create(
            news_title=self.msg["news_title"],
            news_content=self.msg["news_content"],
            publish_time=timezone.now()
        )
        if not new_news:
            raise MsgError(0, 'fail to create a news')


class NewsDetail(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_id")
        try:
            detail = News.objects.filter(id=self.msg["news_id"]).values('news_title', 'news_content', 'publish_time')
            a = (list(detail))[0]
            # json无法序列化datetime
            a['publish_time'] = a['publish_time'].timestamp()
            return json.dumps(a)
        except:
            raise MsgError(0, 'news does not exist')
            

class NewsDelete(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("news_id")
        try:
            News.objects.get(id=self.msg["news_id"]).delete()
        except:
            raise MsgError(0, 'fail to delete a news')


class FeedbackList(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("read_status")
        try:
            temp = Feedback.objects.filter(read_status=self.msg['read_status']).values(
                'feedback_title', 'id', 'user', 'feedback_time')
            a = list(temp)
            for i in a:
                i['feedback_time'] = i['feedback_time'].timestamp()
            return json.dumps({'feedback_list': json.dumps(a)})
        except:
            raise MsgError(0, 'fail to list feedback')


class FeedbackDetail(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        self.checkMsg("feedback_id")
        try:
            temp = Feedback.objects.filter(id=self.msg['feedback_id']).values(
                'feedback_title', 'feedback_content', 'feedback_time', 'user')
            a = list(temp)[0]
            a['feedback_time'] = a['feedback_time'].timestamp()
            return json.dumps(a)
        except:
            raise MsgError(0, 'cannot get the detail of this feedback')


class UserUpdate(APIView):

    def get(self):
        if not self.request.user.is_authenticated:
            raise MsgError(0, 'not login')
        pass