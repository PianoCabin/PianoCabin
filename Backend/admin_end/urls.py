from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view()),
    path('logout/', Logout.as_view()),
    path('piano-room/create/', PianoRoomCreate.as_view()),
    path('piano-room/edit/', PianoRoomEdit.as_view()),
    path('piano-room/list/', PianoRoomList.as_view()),
    path('order/list/', OrderList.as_view()),
    path('news/list/', NewsList.as_view()),
    path('news/create/', NewsCreate.as_view()),
    path('news/detail/', NewsDetail.as_view()),
    path('news/delete/', NewsDelete.as_view()),
    path('feedback/list/', FeedbackList.as_view()),
    path('feedback/detail/', FeedbackDetail.as_view()),
    path('user/update/', UserUpdate.as_view()),
    path('user/list/', UserList.as_view()),
    path('user/edit/', UserEdit.as_view()),
]