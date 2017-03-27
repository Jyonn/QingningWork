import json
from configparser import ConfigParser
from urllib.parse import urlencode

import requests
from django.utils.crypto import get_random_string

cf = ConfigParser()
cf.read("../setting.conf")
yunpian_appkey = cf.get("yunpian", "appkey")


class SendMobile:
    @staticmethod
    def send_captcha(mobile):
        text = "【青柠文字社】验证码为#code#，请您在5分钟内填写。如非本人操作，请忽略本短信。"
        code = get_random_string(length=6, allowed_chars="1234567890")
        text = text.replace("#code#", code)
        # print(text)
        SendMobile.send_sms(yunpian_appkey, text, mobile)
        return code

    @staticmethod
    def send_sms(apikey, text, mobile):
        """
        云片短信发送API
        :param apikey: 云片应用密钥
        :param text: 发送明文
        :param mobile: 11位手机号
        :return:
        """
        # 服务地址
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        params = urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        response = requests.post(url, params, headers=headers)
        response_str = response.text
        response.close()
        # print(response_str)
        return json.loads(response_str)

# print(SendMobile.send_captcha("17816871961"))
