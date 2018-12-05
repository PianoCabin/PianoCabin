from django.views.generic import View
from django.shortcuts import render
from django.http import Http404
import re


class Page(View):
    def dispatch(self, request, *args, **kwargs):
        page = kwargs.get('page')
        page = page.replace('..', '.')
        page += '.html'
        try:
            return render(request, page)
        except:
            raise Http404()


class RoomDetail(View):
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'room-detail.html')

class FeedbackDetail(View):
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'feedback-detail.html')

class NewsCreate(View):
    def dispatch(self, request, *args, **kwargs):
        return render(request, 'news-create.html')