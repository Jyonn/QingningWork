# coding=utf-8
import datetime
from multiprocessing import TimeoutError

from django.http import HttpResponse
from AbstractUser.models import AbstractUser
import json
import re

from BaseFunc.error import Error
from Reviewer.models import Reviewer
from Writer.models import Writer


def work_belongs(work, o_user):
    return (work.re_reviewer == o_user and work.re_writer is None) or work.re_writer == o_user


def username_regex(username):
    # r = r'[A-Za-z]\w{5,19}'
    # r = r'\w{6,20}'
    # return re.fullmatch(r, username) is not None
    return 2 <= len(username) <= 20


def password_regex(password):
    r = r'[-\w!@#$%^&*_]{6,20}'
    return re.fullmatch(r, password) is not None


def get_chinese_date_string(d):
    month_str = "零壹贰叁肆伍陆柒捌玖拾"
    date_string = ""
    if d.month >= 10:
        date_string = month_str[10]
    t = d.month % 10
    if t > 0:
        date_string += month_str[t]
    date_string += "月"
    t = d.day
    if t >= 30:
        date_string += month_str[3]
    elif t >= 20:
        date_string += month_str[2]
    if t >= 10:
        date_string += month_str[10]
    t = t % 10
    if t > 0:
        date_string += month_str[t]
    date_string += '日'
    return date_string


def get_normal_date_string(d):
    return str(d.year) + '/' + str(d.month) + '/' + str(d.day)


def get_readable_time_string(t):
    crt_date = datetime.datetime.now().date()
    ret_str = ''
    if crt_date.year != t.year:
        ret_str = str(t.year) + '年'
    if crt_date.year != t.year or crt_date.month != t.month or crt_date.day != t.day:
        ret_str += str(t.month) + "月" + str(t.day) + '日 '
    ret_str += str(t.hour) + ':' + str(t.minute)

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
        except TimeoutError:
            return "无法获取"
        except Exception:
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


def save_session(request, key, value):
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value


def save_captcha(request, captcha_type, code, last=300):
    """
    保存验证码
    :param request:
    :param last: 有效期限
    :param captcha_type: 验证码类型，分为 image_register, image_forget 和 phone_register, phone_forget
    :param code: 验证码值
    :return: None
    """
    save_session(request, "captcha_" + captcha_type + "_code", str(code))
    save_session(request, "captcha_" + captcha_type + "_time", int(datetime.datetime.now().timestamp()))
    save_session(request, "captcha_" + captcha_type + "_last", last)
    return None


def check_captcha(request, captcha_name, code):
    """
    检验验证码
    :param request:
    :param captcha_name: 验证码类型，分为 image, image_forget 和 phone
    :param code: 验证码值
    :return: 相同返回True, 不同返回False
    """
    correct_code = load_session(request, "captcha_" + captcha_name + "_code")
    correct_time = load_session(request, "captcha_" + captcha_name + "_time")
    correct_last = load_session(request, "captcha_" + captcha_name + "_last")
    current_time = int(datetime.datetime.now().timestamp())

    try:
        del request.session["captcha_" + captcha_name + "_code"]
        del request.session["captcha_" + captcha_name + "_time"]
        del request.session["captcha_" + captcha_name + "_last"]
    except:
        pass
    if None in [correct_code, correct_time, correct_last]:
        return False
    if current_time - correct_time > correct_last:
        return False
    return correct_code.upper() == str(code).upper()


def login_to_session(request, user):
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
    save_session(request, 'user', user.uid)
    return None


def get_user_from_session(request):
    """
    从Session中获取保存的用户
    :param request:
    :return: Reviewer或Writer类
    """
    user_pk = load_session(request, 'user', once_delete=False)
    if user_pk is None:
        return None
    try:
        o_user = AbstractUser.objects.get(pk=user_pk)
        if o_user.user_type == AbstractUser.TYPE_WRITER:
            return Writer.objects.get(pk=o_user.user_id)
        elif o_user.user_type == AbstractUser.TYPE_REVIEWER:
            return Reviewer.objects.get(pk=o_user.user_id)
        else:
            return None
    except:
        return None


def logout_from_session(request):
    """
    登出系统，销毁session
    """
    load_session(request, 'user', once_delete=True)
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


def error_response(error_id, append_msg=""):
    for error in Error.ERROR_DICT:
        if error_id == error[0]:
            return response(code=error_id, msg=error[1]+append_msg)
    return error_response(Error.NOT_FOUND_ERROR)
