

import hashlib,base64
import random,string

import requests

from web.application import app


class MemberService():
    """
    """

    @staticmethod
    def setAuthcode(member_info):
        m = hashlib.md5()
        str = "%s-%s-%s" % (member_info.id, member_info.salt, member_info.status )
        m.update(str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def setSalt(length=16):
        keylist = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(keylist)

    @staticmethod
    def getWeChatOpenID(code):
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code' \
            .format(app.config['APPID'], app.config['API_SECRET'], code)
        r = requests.get(url)
        res = r.json()
        openid = None
        if 'openid' in res:
            openid = res['openid']
        return openid