# coding=utf-8
import base64

from BaseFunc.base import *
from functools import wraps
from AbstractUser.models import AbstractUser
from django.views.decorators import http

require_POST = http.require_POST
require_GET = http.require_GET


def require_params(need_params, decode=True):
    """
    需要获取的参数是否在request.POST中存在
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for need_param in need_params:
                if need_param in request.POST:
                    if decode:
                        x = request.POST[need_param]
                        c = base64.decodebytes(bytes(x, encoding='utf8')).decode()
                        request.POST[need_param] = c
                else:
                    return error_response(Error.REQUIRE_PARAM, append_msg=need_param)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_json(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.body:
            try:
                request.POST = json.loads(request.body.decode())
            except:
                pass
            return func(request, *args, **kwargs)
        else:
            return error_response(Error.REQUIRE_JSON)

    return wrapper


def decorator_generator(verify_func, error_id):
    """
    装饰器生成器
    """

    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if verify_func(request):
                return func(request, *args, **kwargs)
            return error_response(error_id)
        return wrapper
    return decorator


def require_login_func(request):
    o_user = get_user_from_session(request)
    return o_user is not None


def deny_login_func(request):
    return not require_login_func(request)

require_login = decorator_generator(require_login_func, Error.REQUIRE_LOGIN)
deny_login = decorator_generator(deny_login_func, Error.DENY_LOGIN)


def require_login_writer_func(request):
    ret = require_login_func(request)
    if ret is not True:
        return False
    return request.session["role_type"] == AbstractUser.WRITER


def require_login_reviewer_func(request):
    ret = require_login_func(request)
    if ret is not True:
        return False
    return request.session["role_type"] == AbstractUser.REVIEWER

require_login_writer = decorator_generator(require_login_writer_func, Error.REQUIRE_WRITER)
require_login_reviewer = decorator_generator(require_login_reviewer_func, Error.REQUIRE_REVIEWER)
