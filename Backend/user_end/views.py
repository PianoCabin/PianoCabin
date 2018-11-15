from utils.utils import *
from admin_end.models import *
from datetime import datetime
import json
import jwt
import requests
from urllib import parse


# Create your views here.
class Login(APIView):
    # login API
    def get(self):
        self.getUserBySession()

    def post(self):
        self.checkMsg('code')
        code = self.msg.get('code')
        data = {
            'appid': CONFIGS['APP_ID'],
            'secret': CONFIGS['APP_SECRET'],
            'js_code': code,
            'grant_type': 'authorization_code'
        }
        res = requests.get(url='https://api.weixin.qq.com/sns/jscode2session', params=data)
        res = json.loads(res.text)
        if 'openid' not in res:
            raise MsgError(msg='Invalid code')
        else:
            open_id = res['openid']
            user = User.objects.create(open_id=open_id)
            if user is None:
                raise MsgError(msg='Creating user fails')
            payload = {
                'iat': datetime.utcnow(),
                'iss': 'PianoCabin',
                'openid': open_id
            }
            session = jwt.encode(payload=payload, key=CONFIGS['APP_SECRET'], algorithm='HS256')
            session_user.set(session, user.id)


class Bind(APIView):
    # bind API

    def get(self):
        self.checkMsg('ticket', 'authorization')
        ticket = self.msg.get('ticket')
        user = self.getUserBySession()
        url = 'https://id.tsinghua.edu.cn/thuser/authapi/checkticket/{AppID}/{ticket}/{UserIpAddr}'
        url = parse.urljoin(url, CONFIGS['THU_APP_ID'])
        url = parse.urljoin(url, ticket)
        url = parse.urljoin(url, CONFIGS['DOMAIN'].replace('.', '_'))
        res = requests.get(url=url)
        try:
            info = json.loads(res.text)
            if info.get('code') != 0:
                raise MsgError
            else:
                user.identity = info.get('zjh')
                if info.get('yhlb') in ['J0000', 'H0000', 'J0054']:
                    user.permission = 1
                elif info.get('yhlb') in ['X0011', 'X0021', 'X0031']:
                    user.permission = 2
                user.save()
        except:
            raise MsgError('Invalid ticket')

