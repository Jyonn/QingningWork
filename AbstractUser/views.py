from pydoc import html

from Base.decorator import *
from QingningWork.settings import WORK_URL
from Reviewer.models import Reviewer
from Work.models import Work
from Writer.models import Writer


@require_POST
@require_json
@require_params(["username", "password"])
@deny_login
def login(request):
    """
    登录系统
    """
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        reviewer = Reviewer.objects.get(username=username)
        if reviewer.pwd_login:  # 未开启免密登录，需要验证密码
            if not reviewer.check_password(password):
                return error_response(Error.WRONG_PASSWORD)
        login_to_session(request, reviewer, AbstractUser.REVIEWER)
        return response()
    except Exception as e:
        print(Exception, ":", e)

    try:
        writer = Writer.objects.get(username=username)
        if writer.pwd_login:
            if not writer.check_password(password):
                return error_response(Error.WRONG_PASSWORD)
        login_to_session(request, writer, AbstractUser.WRITER)
        return response()
    except Exception as e:
        print(Exception, ":", e)

    return error_response(Error.NOT_FOUND_USERNAME)


@require_POST
@require_json
@require_params(["username", "password"])
@require_login
def change_username(request):
    username = request.POST["username"]
    password = request.POST["password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.UNKNOWN)
    if user.pwd_login:
        if not user.check_password(password):
            return error_response(Error.WRONG_PASSWORD)
    user.username = username
    user.save()
    return response()


@require_POST
@require_json
@require_params(["old_password", "new_password"])
@require_login
def change_password(request):
    old_password = request.POST["old_password"]
    new_password = request.POST["new_password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.UNKNOWN)
    if user.pwd_login:
        if not user.check_password(old_password):
            return error_response(Error.WRONG_PASSWORD)
    else:
        user.pwd_login = True
    user.set_password(new_password)
    user.save()
    return response()


@require_POST
@require_json
@require_params(["password"])
@require_login
def unset_password(request):
    password = request.POST["password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.UNKNOWN)
    if not user.pwd_login:
        return error_response(Error.NO_PASSWORD_LOGIN)
    if not user.check_password(password):
        return error_response(Error.WRONG_PASSWORD)
    user.pwd_login = False
    user.save()
    return response()


@require_POST
@require_login
def logout(request):
    logout_from_session(request)
    return response()
