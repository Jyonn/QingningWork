import datetime

from Base.decorator import *
from Reviewer.models import Reviewer
from Writer.models import Writer
from AbstractUser.models import LikeUser


def get_user_by_id(uid):
    try:
        user = AbstractUser.objects.get(pk=uid)
    except:
        return None, Error.NOT_FOUND_USER_ID
    if user.is_frozen is True:
        return None, Error.FROZEN_USER
    return user, Error.OK


@require_POST
@require_json
@require_params(["username", "password", "no_pwd"])
def register(request):
    """
    注册系统
    """
    username = request.POST["username"]
    password = request.POST["password"]
    pwd_login = request.POST["no_pwd"] is True
    if AbstractUser.objects.filter(username=username).count() >= 1:
        return error_response(Error.EXIST_USERNAME)

    writer = Writer.create(
        username=username,
        pwd_login=pwd_login,
    )
    if pwd_login is True:
        writer.set_password(password).save()
    login_to_session(request, writer, AbstractUser.WRITER)
    return response(body=AbstractUser.WRITER)


@require_POST
@require_json
@require_params(["username", "password", "no_pwd"])
def add_reviewer(request):
    """
    添加审稿员
    """
    username = request.POST["username"]
    password = request.POST["password"]
    pwd_login = request.POST["no_pwd"] is True
    if AbstractUser.objects.filter(username=username).count() >= 1:
        return error_response(Error.EXIST_USERNAME)

    reviewer = Reviewer.create(
        username=username,
        pwd_login=pwd_login,
    )
    if pwd_login is True:
        reviewer.set_password(password).save()
    login_to_session(request, writer, AbstractUser.WRITER)
    return response(body=AbstractUser.WRITER)


@require_POST
@require_json
@require_params(["username", "password"])
# @deny_login
def login(request):
    """
    登录系统
    """
    username = request.POST["username"]
    password = request.POST["password"]

    try:
        reviewer = Reviewer.objects.get(username=username)
        if reviewer.is_frozen is True:
            return error_response(Error.FROZEN_USER)
        if reviewer.pwd_login:  # 未开启免密登录，需要验证密码
            if not reviewer.check_password(password):
                return error_response(Error.WRONG_PASSWORD)
        login_to_session(request, reviewer, AbstractUser.REVIEWER)
        return response(body=AbstractUser.REVIEWER)
    except Exception as e:
        print(Exception, ":", e)

    try:
        writer = Writer.objects.get(username=username)
        if writer.pwd_login:
            if not writer.check_password(password):
                return error_response(Error.WRONG_PASSWORD)
        login_to_session(request, writer, AbstractUser.WRITER)
        return response(body=AbstractUser.WRITER)
    except Exception as e:
        print(Exception, ":", e)

    return error_response(Error.NOT_FOUND_USERNAME)


@require_POST
@require_json
@require_params(["old_username", "new_username", "password"])
@require_login
def change_username(request):
    """
    修改用户账号
    """
    old_username = request.POST["old_username"]
    new_username = request.POST["new_username"]
    password = request.POST["password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
    if user.pwd_login:
        if not user.check_password(password):
            return error_response(Error.WRONG_PASSWORD)
    else:
        if user.username != old_username:
            return error_response(Error.WRONG_USERNAME)
    user.username = new_username
    user.save()
    return response()


@require_POST
@require_json
@require_params(["old_password", "new_password"])
@require_login
def change_password(request):
    """
    修改用户密码
    """
    old_password = request.POST["old_password"]
    new_password = request.POST["new_password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
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
    """
    当前用户设为免密模式
    """
    password = request.POST["password"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.UNKNOWN)
    if not user.pwd_login:  # 检查是否已经是免密模式
        return error_response(Error.NO_PASSWORD_LOGIN)
    if not user.check_password(password):  # 检查密码是否正确
        return error_response(Error.WRONG_PASSWORD)
    print("true");
    user.pwd_login = False
    user.save()
    print(user.pwd_login)
    return response()


@require_POST
@require_login
def logout(request):
    """
    登出系统
    """
    logout_from_session(request)
    return response()


@require_POST
def status(request):
    """
    获取当前用户状态（未登录，已登录）
    """
    if require_login_func(request):
        user, user_type = get_user_from_session(request)
        if user is None:
            return error_response(Error.LOGIN_AGAIN)
        return response(body=user_type)
    else:
        return response()


@require_POST
@require_login
def upload_prepare(request):
    now = datetime.datetime.now()
    user, user_type = get_user_from_session(request)
    if user is not None and user_type == "writer":
        writer_name = user.nickname
    else:
        writer_name = None
    return response(body=dict(
        writer_name=writer_name,
        current_time=get_readable_time_string(now),
    ))


@require_POST
@require_login
def get_info(request):
    """
    获取个人信息
    response
    {
        type: 用户类型
        nickname: 昵称 / 笔名
        pwd_login: 是否免密
        phone: 手机号
        email: 邮箱
        avatar: 头像
    }
    """
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
    return_dict = dict(
        type=user_type,
        nickname=user.nickname,
        pwd_login=user.pwd_login,
        phone=user.phone,
        email=user.email,
        avatar=user.avatar,
    )
    return response(body=return_dict)


@require_POST
@require_json
@require_params(["nickname"])
@require_login
def set_basic_info(request):
    """
    修改用户基本信息
    """
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
    nickname = request.POST["nickname"]
    nickname = ''.join(nickname.split(' '))
    if len(nickname) > 6:
        return error_response(Error.NICKNAME_TOO_LONG)
    try:
        user.nickname = nickname
        user.save()
    except:
        return error_response(Error.EXIST_NICKNAME)
    return response()


@require_POST
@require_json
@require_params(["uid"])
@require_login
def reverse_like(request):
    uid = request.POST["uid"]
    user, user_type = get_abstract_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
    user_liked, ret_code = get_user_by_id(uid)
    if ret_code != Error.OK:
        return error_response(ret_code)
    try:
        like_user = LikeUser.objects.get(
            re_user_liked=user_liked,
            re_user_to_like=user,
        )
    except:
        like_user = LikeUser.create(
            re_user_liked=user_liked,
            re_user_to_like=user,
            result=None,
        )
    if like_user.result is None:
        like_user.result = True
        user_liked.total_likes += 1
    elif like_user.result is True:
        like_user.result = None
        user_liked.total_likes -= 1
    like_user.save()
    user_liked.save()

    return response(body=dict(
        result=like_user.result,
        like_number=user_liked.total_likes,
    ))
