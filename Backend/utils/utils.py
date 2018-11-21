from django.http import HttpResponse
from django.views.generic import View
from urllib import parse, request
from Backend.settings import *
from admin_end.models import *
import json
import jwt
import traceback


class APIView(View):
    # API基类

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.msg = self.queryMsg()
        handler = getattr(self, self.request.method.lower(), None)
        if handler is None:
            return self.http_method_not_allowed()
        return self.handleMsg(handler, *args, **kwargs)

    # 提取请求体
    def queryMsg(self):
        msg = getattr(self.request, self.request.method, None)
        if msg:
            msg = msg.dict()
        else:
            msg = {}
        msg.update(self.request.FILES)
        if not msg:
            try:
                msg = json.loads(self.request.body.decode())
            except:
                msg = {}
        msg['authorization'] = self.request.META.get('HTTP_AUTHORIZATION')
        return msg

    # 处理不同请求类型并包装返回值
    def handleMsg(self, handler, *args, **kwargs):
        code = 1
        msg = ''
        data = None
        try:
            data = handler(*args, **kwargs)
        except MsgError as e:
            code = e.code
            msg = e.msg
            print(e.msg)
        except Exception as e:
            code = 0
            msg = str(e)
            traceback.print_exc()
        try:
            response = json.dumps({
                'code': code,
                'msg': msg,
                'data': data,
            })
        except:
            response = json.dumps({
                'code': 0,
                'msg': 'JSON Error',
                'data': None,
            })
        return HttpResponse(response, content_type='application/json')

    # 检查输入
    def checkMsg(self, *keys):
        for k in keys:
            if k not in self.msg:
                raise MsgError(msg='API requires field "%s"' % (k,))

    # 检查多个可选输入
    def checkMsgMultiOption(self, *keys):

        count = 0
        for k in keys:
            if k in self.msg:
                count += 1
        if count == 0:
            raise MsgError(msg='API requires field not enough')

    # 解析session获取用户
    def getUserBySession(self):
        """
        :return: :class:`User <User>` object
        """
        id = redis_manage.session_user.get(self.msg['authorization'])
        if id is None:
            raise MsgError(msg='No such person')
        else:
            user = get_or_none(User, id=int(id.decode()))
            if user is None:
                raise MsgError(msg='User does not exist')
            else:
                return user

    def http_method_not_allowed(self, *args, **kwargs):
        return super().http_method_not_allowed(self.request, *args, **kwargs)


class MsgError(Exception):
    # 自定义的错误信息

    def __init__(self, code=0, msg='Unknown error'):
        super().__init__(msg)
        self.code = code
        self.msg = msg


