# coding=utf-8

from BaseFunc.decorator import *
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
@require_params(['username', 'password', 'captcha'])
def register(request):
    """
    注册作者账号
    :return 0 OK
            1030 用户名存在非法字符，或长度不在6-20位之间
            1031 密码存在非法字符，或长度不在6-20位之间
            1029 错误的验证码
            1021 已存在的用户名
    """
    username = request.POST['username']
    password = request.POST['password']
    captcha = request.POST['captcha']

    if not username_regex(username):
        return error_response(Error.USERNAME_MATCH_ERROR)
    if not password_regex(password):
        return error_response(Error.PASSWORD_MATCH_ERROR)

    if not check_captcha(request, 'image', captcha):
        return error_response(Error.WRONG_CAPTCHA)

    try:
        AbstractUser.objects.get(username=username)
        return error_response(Error.EXIST_USERNAME)
    except:
        pass

    writer = Writer.create(username=username)
    writer.set_password(password).save()
    login_to_session(request, writer)
    return response()


@require_POST
@require_json
@require_params(['username', 'password'])
def add_reviewer(request):
    """
    添加审稿员
    """
    username = request.POST['username']
    password = request.POST['password']
    try:
        AbstractUser.objects.get(username=username)
        return error_response(Error.EXIST_USERNAME)
    except:
        pass

    reviewer = Reviewer.create(
        username=username,
        pwd_login=True,
    )
    reviewer.set_password(password).save()
    login_to_session(request, reviewer)
    return response(body=AbstractUser.WRITER)


@require_POST
@require_json
@require_params(['username', 'password', 'captcha'])
def login(request):
    """
    登录系统
    :return 0 OK
            1029 错误的验证码
            1017 账号被冻结，请联系社长
            1004 用户名或密码错误
            1003 不存在的用户名
    """
    username = request.POST['username']
    password = request.POST['password']
    captcha = request.POST['captcha']

    if not check_captcha(request, 'image', captcha):
        return error_response(Error.WRONG_CAPTCHA)

    try:
        o_user = AbstractUser.objects.get(username=username)
        if o_user.is_frozen:
            return error_response(Error.FROZEN_USER)
        if o_user.pwd_login:
            if not o_user.check_password(password):
                return error_response(Error.WRONG_PASSWORD)
        login_to_session(request, o_user)
        return response()
    except:
        return error_response(Error.NOT_FOUND_USERNAME)


@require_POST
@require_json
@require_params(['old_username', 'new_username', 'password'])
@require_login
def change_username(request):
    """
    修改用户账号
    """
    old_username = request.POST['old_username']
    new_username = request.POST['new_username']
    password = request.POST['password']
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
@require_params(['old_password', 'new_password'])
@require_login
def change_password(request):
    """
    修改用户密码
    """
    old_password = request.POST['old_password']
    new_password = request.POST['new_password']
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
@require_params(['password'])
@require_login
def unset_password(request):
    """
    当前用户设为免密模式
    """
    password = request.POST['password']
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.UNKNOWN)
    if not user.pwd_login:  # 检查是否已经是免密模式
        return error_response(Error.NO_PASSWORD_LOGIN)
    if not user.check_password(password):  # 检查密码是否正确
        return error_response(Error.WRONG_PASSWORD)
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
    if user is not None and user_type == 'writer':
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
@require_params(['nickname'])
@require_login
def set_basic_info(request):
    """
    修改用户基本信息
    """
    user, user_type = get_user_from_session(request)
    if user is None:
        return error_response(Error.LOGIN_AGAIN)
    nickname = request.POST['nickname']
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
@require_params(['uid'])
@require_login
def reverse_like(request):
    uid = request.POST['uid']
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
