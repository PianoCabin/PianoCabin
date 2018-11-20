from django.urls import path
from .views import *

urlpatterns = [
    path('login/', Login.as_view()),
    path('bind/', Bind.as_view()),
    path('order/list/', OrderList.as_view()),
    path('feedback/', CreateFeedBack.as_view()),
    path('order/piano-rooms-list/', PianoRoomList.as_view()),
    path('order/normal/', OrderNormal.as_view()),
    path('order/change', OrderChange.as_view()),
    path('order/cancel', OrderCancel.as_view())
]