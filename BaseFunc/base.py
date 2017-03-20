import datetime
from django.http import HttpResponse
from AbstractUser.models import AbstractUser
from Writer.models import Writer
from Reviewer.models import Reviewer
import json

from BaseFunc.error import Error


def get_readable_time_string(t):
    ret_str = str(t.year) + "年"
    if t.month < 10:
        ret_str += "0"
    ret_str += str(t.month) + "月"
    if t.day < 10:
        ret_str += "0"
    ret_str += str(t.day) + "日 "
    if t.hour < 10:
        ret_str += "0"
    ret_str += str(t.hour) + "时"
    if t.minute < 10:
        ret_str += "0"
    ret_str += str(t.minute) + "分"

    return ret_str


def get_address_by_ip_via_tb(ipv4, timeout=0.5):
    """
    使用淘宝接口根据IP地址获取大致地理位置
    """
    ip_str = ""
    try:
        import requests
        url = "http://ip.taobao.com/service/getIpInfo.php?ip=" + ipv4
        headers = {'content-type': 'application/json'}
        ret_pos = requests.get(url, headers=headers, timeout=timeout).json()
        if ret_pos["code"] != 0:
            ip_str = "未知地址"
        else:
            if ret_pos["data"]["country_id"] != "CN":
                ip_str = ret_pos["data"]["country"]
            if ret_pos["data"]["region_id"] != "":
                ip_str += ret_pos["data"]["region"]
            if ret_pos["data"]["city_id"] != "":
                ip_str += ret_pos["data"]["city"]
    except:
        ip_str = "无法获取"
    return ip_str


def get_address_by_ip_via_sina(ipv4, timeout=0.5):
    """
    使用新浪接口根据IP地址获取大致地理位置
    """
    ip_str = ""
    try:
        import requests
        url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=json&ip=" + ipv4
        headers = {'content-type': 'application/json'}
        try:
            ret_pos = requests.get(url, headers=headers, timeout=timeout).json()
        except TimeoutError as e:
            return "无法获取"
        except Exception as e:
            return "未知地址"
        if ret_pos["country"] != "中国":
            ip_str = ret_pos["country"]
        if ret_pos["province"] != "":
            ip_str += ret_pos["province"]
        if ret_pos["city"] not in ["", ret_pos["province"]]:
            ip_str += ret_pos["city"]
    except:
        ip_str = "未知地址"
    return ip_str


def save_captcha(request, type, code):
    """
    保存验证码
    :param request:
    :param type: 验证码类型，分为 image 和 phone
    :param code: 验证码值
    :return: None
    """
    request.session["captcha_" + type + "_code"] = code
    request.session["captcha_" + type + "_time"] = int(datetime.datetime.now().timestamp())
    return None


def confirm_captcha(request, type, code):
    """
    验证验证码
    :param request:
    :param type: 验证码类型，分为 image 和 phone
    :param code: 输入的验证码值
    :return: True / False
    """
    try:
        if code is None:
            return False
        this_time = int(datetime.datetime.now().timestamp())
        last_time = request.session["captcha_" + type + "_time"]
        dist = this_time - last_time
        if dist > 60 * 5 or dist < 0:
            return False
        correct_captcha = request.session["captcha_" + type + "_code"]
        if correct_captcha != code:
            request.session["captcha_" + type + "_code"] = None
            return False
        else:
            return True
    except:
        pass
    return False


def login_to_session(request, user, user_type):
    """
    更新登录数据并添加到session
    """
    user.login_times += 1
    user.last_login = user.this_login
    user.last_ipv4 = user.this_ipv4
    user.this_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.this_ipv4 = request.META['HTTP_X_FORWARDED_FOR'] \
        if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']
    user.save()

    try:
        request.session.cycle_key()
    except:
        pass
    request.session["role_id"] = user.pk
    request.session["role_type"] = user_type
    request.session["login_in"] = True
    return None


def get_abstract_user_from_session(request):
    if request.session["role_type"] == AbstractUser.WRITER:
        try:
            user = Writer.objects.get(pk=request.session["role_id"])
            user = AbstractUser.objects.get(pk=user.uid)
        except Exception as e:
            print(Exception, ":", e)
            return None, None
        return user, AbstractUser.WRITER
    elif request.session["role_type"] == AbstractUser.REVIEWER:
        try:
            user = Reviewer.objects.get(pk=request.session["role_id"])
            user = AbstractUser.objects.get(pk=user.uid)
        except Exception as e:
            print(Exception, ":", e)
            return None, None
        return user, AbstractUser.REVIEWER
    else:
        return None, None


def get_user_from_session(request):
    try:
        if request.session["role_type"] == AbstractUser.WRITER:
            user = Writer.objects.get(pk=request.session["role_id"])
            return user, AbstractUser.WRITER
        elif request.session["role_type"] == AbstractUser.REVIEWER:
            user = Reviewer.objects.get(pk=request.session["role_id"])
            return user, AbstractUser.REVIEWER
    except:
        pass
    return None, None


def logout_from_session(request):
    """
    登出系统，销毁session
    """
    del request.session["role_id"]
    del request.session["role_type"]
    del request.session["login_in"]
    request.session.flush()
    return None


def response(code=0, msg="ok", body=None):
    resp = {
        "code": code,
        "msg": msg,
        "body": body or [],
    }

    http_resp = HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status=200,
        content_type="application/json; encoding=utf-8",
    )
    return http_resp


def error_response(error_id):
    for error in Error.ERROR_DICT:
        if error_id == error[0]:
            return response(code=error_id, msg=error[1])
    return error_response(Error.NOT_FOUND_ERROR)
