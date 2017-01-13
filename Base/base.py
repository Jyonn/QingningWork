from django.http import HttpResponse
from AbstractUser.models import AbstractUser
from Writer.models import Writer
from Reviewer.models import Reviewer
import json

from Base.error import Error


def login_to_session(request, user, user_type):
    """
    更新登录数据并添加到session
    """
    import datetime
    user.last_login = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user.last_ipv4 = request.META['HTTP_X_FORWARDED_FOR'] \
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


def get_user_from_session(request):
    if request.session["role_type"] == AbstractUser.WRITER:
        try:
            user = Writer.objects.get(pk=request.session["role_id"])
        except Exception as e:
            print(Exception, ":", e)
            return None, None
        return user, AbstractUser.WRITER
    elif request.session["role_type"] == AbstractUser.REVIEWER:
        try:
            user = Reviewer.objects.get(pk=request.session["role_id"])
        except Exception as e:
            print(Exception, ":", e)
            return None, None
        return user, AbstractUser.REVIEWER
    else:
        return None, None


def logout_from_session(request):
    """
    登出系统，销毁session
    """
    del request.session["role_id"]
    del request.session["role_type"]
    request.session["login_in"] = False
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
