"""

由于需要开通微信支付 所以此功能只能进行书写  而没有验证
没有商家号  不能做处理，但是可以模拟

"""
import datetime
import hashlib
import json
import uuid
import xml.etree.ElementTree as ET

from common.libs.Helper import getCurrentDate
from common.models.pay.OauthAccessToken import OauthAccessToken
from web.application import app, db

import requests


class WeChatService():
    def __init__(self, merchant_key=None):
        # 微信支付秘钥
        self.mechant_key = merchant_key

    def create_sign(self,pay_data):
        """
        生成签名 signA
        :param pay_data:
        :return:
        https://pay.weixin.qq.com/wiki/doc/api/wxa/wxa_api.php?chapter=4_3 根据此网页 返回对应数据
        """
        stringA = "&".join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = "{0}&key={1}".format(stringA, self.mechant_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()

        return sign.upper()


    def get_pay_info(self, pay_data=None):
        """
        获取支付信息
        根据微信支付接口数据进行返回拼接
        :return:
        """
        sign = self.create_sign(pay_data)
        pay_data['sign'] = sign
        xml_data = self.dict_to_xml(pay_data)
        # 微信统一下单地址
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        headers = {
            "Content-Type":"application/xml"
        }
        r = requests.post(url, data=xml_data.encode("utf-8"), headers=headers)
        r.encoding = "utf-8"

        app.logger.info(r.text)
        if r.status_code == 200:
            prepay_id = self.xml_to_dict(r.text).get('prepay_id')
            pay_sign_data = {
                'appId':pay_data.get('appid'),
                'timeStamp':pay_data.get('out_trade_no'),
                'nonceStr':pay_data.get('nonce_str'),
                'package': 'prepay_id={0}'.format(prepay_id),
                'signType': 'MD5'
            }
            pay_sign = self.create_sign(pay_sign_data)
            pay_sign_data.pop('appId')
            pay_sign_data['paySign'] = pay_sign
            pay_sign_data['prepay_id'] = prepay_id

            return pay_sign_data
        return False

    def dict_to_xml(self, dict_data):
        """
        返回指定的xml格式数据
        :param dict_data:
        :return:
        """
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k,v))
        xml.append("</xml>")

        return  "".join(xml)


    def xml_to_dict(self, xml_data):
        """
        下完单 需要将xml数据转换 dict
        :param xml_data:
        :return:
        """
        xml_dict = {}

        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict

    def get_nonce_str(self):
        return str(uuid.uuid4()).replace("-","")


    def getAccessToken(self):
        """
        获取AccessToken方法
        :return:
        """
        token = None
        token_info = OauthAccessToken.query.filter(OauthAccessToken.expired_time >= getCurrentDate()).first()
        if token_info:
            token = token_info.access_token
        config_mima = app.config['MINA_APP']
        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={0}&secret={1}'.\
            format(config_mima['appid'], config_mima['appkey'])

        r = requests.get(url)
        if r.status_code !=200 or not r.text:
            return token
        data = r.json()

        # 存储token
        now =datetime.datetime.now()
        date = now + datetime.timedelta(seconds=data['expires_in'] - 200)
        model_token = OauthAccessToken()
        model_token.access_token = data['access_token']
        model_token.expired_time = date.strftime("%Y-%m-%d %H:%M:%S")
        model_token.created_time=getCurrentDate()
        db.session.add(model_token)
        db.session.commit()

        return data['access_token']