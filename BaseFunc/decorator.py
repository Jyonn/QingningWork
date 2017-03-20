# coding=utf-8
from BaseFunc.base import *
from functools import wraps
from AbstractUser.models import AbstractUser
from django.views.decorators import http

require_POST = http.require_POST
require_GET = http.require_GET


def require_params(need_params):
    """
    需要获取的参数是否在request.POST中存在
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for need_param in need_params:
                if need_param not in request.POST:
                    return error_response(Error.NEED_PARAM)
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
            return error_response(Error.NEED_JSON)

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
    if "login_in" not in request.session or "role_id" not in request.session or "role_type" not in request.session:
        return False
    if request.session["login_in"] is None or request.session["role_id"] is None \
            or request.session["role_type"] is None:
        return False
    return request.session["login_in"]


def deny_login_func(request):
    return not require_login_func(request)

require_login = decorator_generator(require_login_func, Error.NEED_LOGIN)
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

require_login_writer = decorator_generator(require_login_writer_func, Error.NEED_WRITER)
require_login_reviewer = decorator_generator(require_login_reviewer_func, Error.NEED_REVIEWER)
