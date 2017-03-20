import datetime

from BaseFunc.decorator import *
from Comment.models import Comment
from QingningWork.settings import WORK_URL
from Work.models import Work


def work_is_mine(request, work):
    if require_login_func(request):
        user, user_type = get_user_from_session(request)
        if user is None:
            return False
        if user == work.re_writer:
            return True
        elif user == work.re_reviewer and work.re_writer is None:
            return True
    return False


def get_work_by_id(wid):
    try:
        work = Work.objects.get(pk=wid)
    except:
        return None, Error.NOT_FOUND_WORK_ID
    if work.is_delete is True:
        return None, Error.WORK_HAS_DELETED
    return work, Error.OK


def get_packed_work(work, related_type=None):
    refs_num = Comment.objects.filter(re_work=work, is_updated=False, result=False).count()
    recv_num = Comment.objects.filter(re_work=work, is_updated=False, result=True).count()
    timestamp_now = int(datetime.datetime.now().timestamp())
    timestamp_crt = int(work.create_time.timestamp())
    dist = timestamp_now - timestamp_crt
    if dist < 60:
        dist_str = str(int(dist)) + "秒前"
    elif dist < 60 * 60:
        dist_str = str(int(dist/60)) + "分钟前"
    elif dist < 60 * 60 * 24:
        dist_str = str(int(dist/60/60)) + "小时前"
    elif dist < 60 * 60 * 24 * 30:
        dist_str = str(int(dist/60/60/24)) + "天前"
    elif dist < 60 * 60 * 24 * 365:
        dist_str = str(int(dist/60/60/24/30)) + "个月前"
    else:
        dist_str = str(int(dist/60/60/24/365)) + "年前"

    work_detail = dict(
        wid=work.pk,  # 作品编号
        writer_name=work.writer_name,  # 作者笔名
        work_name=work.work_name,  # 作品名称
        create_time=get_readable_time_string(work.create_time),  # 上传时间
        dist_time=dist_str,
        related_type=related_type,  # 关联类型
        status=work.status,  # 作品状态
        is_public=work.is_public,  # 是否删除
        is_delete=work.is_delete,  # 是否公开
        refs_num=refs_num,  # 过审数
        recv_num=recv_num,  # 驳回数
        version_num=work.version_num,
    )
    if work.re_writer is not None:
        work_detail["re_avatar"] = work.re_writer.avatar
    else:
        work_detail["re_avatar"] = work.re_reviewer.avatar
    return work_detail


@require_POST
@require_json
@require_params(["wid"])
def get_work_detail(request):
    """
    获取作品详细信息
    request
    {
        wid: 作品编号
    }
    response
    {
        wid: 作品编号
        writer_name: 作者名称
        work_name: 作品名称
        create_time: 创建时间
        status: 作品状态，详见 Work 表定义
        fee: 作品稿费，仅当 status 为 STATUS_CONFIRM_FEE 时有效
        work_type: 作品类型
        re_writer_id: 作者编号
        re_reviewer_id: 审稿员编号
        is_mine: 是当前用户的作品
    }
    """
    wid = request.POST["wid"]
    work, ret_code = get_work_by_id(wid)
    if work is None:
        return error_response(ret_code)

    work_detail = dict(
        wid=work.pk,
        writer_name=work.writer_name,
        work_name=work.work_name,
        create_time=get_readable_time_string(work.create_time),
        status=work.status,
        fee=work.fee,
        work_type=work.work_type,
    )
    if work.re_writer is not None:
        work_detail["re_writer_id"] = work.re_writer.pk
    if work.re_reviewer is not None:
        work_detail["re_reviewer_id"] = work.re_reviewer.pk

    work_detail["is_mine"] = work_is_mine(request, work)

    if work.is_public is False and work_detail["is_mine"] is False:
        return error_response(Error.WORK_IS_PRIVATE)

    if work.work_type == Work.WORK_TYPE_TEXT:
        file_path = WORK_URL + work.work_store
        with open(file_path, "rb+") as f:
            content = f.read().decode()
            f.close()
        work_detail["content"] = content
        work_detail["url"] = None
    else:
        work_detail["content"] = None
        work_detail["url"] = "/work/upload_files/" + work.work_store

    return response(body=work_detail)


@require_POST
@require_json
@require_params(["wid"])
def get_work_comments(request):
    """
    获取作品的所有(最新)评论
    response
    {
        rid: 审稿员编号
        nickname: 审稿员昵称
        avatar: 审稿员头像
        content: 评价内容
        result: 评价结果
        comment_time: 评价时间
        times: 评价次数
    }
    """
    wid = request.POST["wid"]
    work, ret_code = get_work_by_id(wid)
    if work is None:
        return error_response(ret_code)
    if work.is_public is False:
        return error_response(Error.WORK_IS_PRIVATE)

    comment_list = []
    comments = Comment.objects.filter(
        re_work=work,
        is_updated=False,
    )
    for comment in comments:
        reviewer_comments = Comment.objects.filter(re_work=work, re_reviewer=comment.re_reviewer)
        comment_list.append(dict(
            rid=comment.re_reviewer.pk,
            nickname=comment.re_reviewer.nickname,
            avatar=comment.re_reviewer.avatar,
            content=comment.content,
            result=comment.result,
            comment_time=get_readable_time_string(comment.comment_time),
            times=reviewer_comments.count(),
        ))

    return response(body=comment_list)


def create_work(request):
    """
    创建作品
    """
    work_type = request.POST["work_type"]  # 作品类型（WORK_TYPE_FILE文件上传; WORK_TYPE_TEXT文本上传）
    work_name = request.POST["work_name"]  # 作品名称，指题目
    writer_name = request.POST["writer_name"]  # 作者名称
    content = request.POST["content"]
    user, user_type = get_user_from_session(request)
    if user is None:
        return None, Error.LOGIN_AGAIN
    if len(work_name) > 20:
        return None, Error.WORK_NAME_TOO_LONG
    if len(writer_name) > 6:
        return None, Error.NICKNAME_TOO_LONG
    
    #  获取作品类型
    try:
        work_type = int(work_type)
    except:
        return None, Error.NOT_FOUND_WORK_TYPE
    if work_type not in [Work.WORK_TYPE_FILE, Work.WORK_TYPE_TEXT]:
        # 不存在的作品类型
        return None, Error.NOT_FOUND_WORK_TYPE

    if work_type == Work.WORK_TYPE_FILE:
        # 如果是文件，获取文件扩展名
        if request.FILES.get("file") is None:
            return None, Error.NOT_FOUND_FILE
        str_name = request.FILES.get("file").name
        ext_name = "" if str_name.find(".") == -1 else "." + str_name.split(".")[-1]
    else:
        # 如果是文本，默认扩展名为txt
        ext_name = ".txt"

    moment = datetime.datetime.now()
    create_time = moment.strftime("%Y-%m-%d %H:%M:%S")  # 创建时间
    head_filename = moment.strftime("%Y%m%d_%H%M%S_")  # 保存文件头
    from django.utils.crypto import get_random_string
    # 保存的文件名设置为上传时间+随机子串+扩展名
    filename = head_filename + get_random_string(length=8) + ext_name[:8]
    # 保存的文件路径
    file_path = WORK_URL + filename

    if work_type == Work.WORK_TYPE_FILE:
        # 上传文件，使用chunk保存
        save_file = request.FILES.get("file")
        with open(file_path, "wb+") as f:
            for chunk in save_file.chunks():
                f.write(chunk)
            f.close()
    else:
        # Base64解码并HTML转义特殊字符后Base64编码
        # import base64
        # content = base64.decodebytes(bytes(content, encoding="utf8"))
        # content = content.decode()
        # from pydoc import html
        # content = html.escape(content)
        # content = base64.encodebytes(bytes(content, encoding="utf-8"))
        content = bytes(content, encoding="utf-8")
        # 保存文本文件
        with open(file_path, "wb+") as f:
            f.write(content)
            f.close()

    # 存入数据库
    work = Work.create(
        writer_name=writer_name,
        work_name=work_name,
        work_store=filename,
        work_type=work_type,
        is_public=True,
        status=Work.STATUS_UNDER_REVIEW,
        create_time=create_time,
    )
    if user_type == AbstractUser.REVIEWER:
        work.re_reviewer = user
        user.total_upload += 1
    else:
        work.re_writer = user
        user.total_works += 1
    user.save()
    work.save()
    return work, Error.OK


def delete_work(work):
    """
    删除作品
    """
    if work.status == Work.STATUS_CONFIRM_FEE:  # 作品被确认收录，无法删除
        return Error.CAN_NOT_DELETE_CAUSE_CONFIRMED
    if work.re_writer is not None:  # 作品属于某作者
        work.re_writer.total_works -= 1  # 作者作品总数-1
        if work.status == Work.STATUS_RECEIVED:  # 作者被采纳作品数-1
            work.re_writer.total_received -= 1
        elif work.status == Work.STATUS_REFUSED:  # 作者被驳回作品数-1
            work.re_writer.total_refused -= 1
        work.re_writer.save()
    elif work.re_reviewer is not None:  # 作品属于某审稿员
        work.re_reviewer.total_upload -= 1  # 审稿员总上传数-1
        work.re_reviewer.save()

    # 获取作品评论
    comments = Comment.objects.filter(re_work=work, is_updated=False)
    for comment in comments:
        # 恢复审稿员的审稿数
        if comment.result is True:
            comment.re_reviewer.total_received -= 1
        else:
            comment.re_reviewer.total_refused -= 1
        comment.re_reviewer.save()

    # 标记删除
    work.is_delete = True
    work.save()
    return Error.OK


@require_POST
@require_json
@require_params(["work_type", "work_name", "writer_name", "content"])
@require_login
def upload_work(request):
    """
    审稿员或作者上传稿件
    request
    {
        work_type: 作品类型，只能为 WORK_TYPE_FILE 或 WORK_TYPE_TEXT
        work_name: 作品名称
        writer_name: 作者名称
        content: 作品正文，当 work_type 为 WORK_TYPE_TEXT 时有效
        file: 上传的作品，当 work_type 为 WORK_TYPE_FILE 时有效
    }
    """
    work, ret_code = create_work(request)
    if ret_code != Error.OK:
        return error_response(ret_code)

    return response(body=work.pk)


@require_POST
@require_json
@require_params(["work_type", "work_name", "writer_name", "content", "wid"])
@require_login
def modify(request):
    """
    修改作品（懒惰删除，保留备份）
    """
    wid = request.POST["wid"]
    work, ret_code = get_work_by_id(wid)
    if work is None:
        return error_response(ret_code)

    # 删除原作品
    ret_code = delete_work(work)
    if ret_code != Error.OK:
        return error_response(ret_code)

    # 创建新作品
    modified_work, ret_code = create_work(request)
    if ret_code != Error.OK:
        return error_response(ret_code)
    modified_work.last_version_work = work
    modified_work.version_num = work.version_num + 1
    modified_work.save()

    return response(body=modified_work.pk)


@require_POST
@require_json
@require_params(["wid"])
@require_login
def delete(request):
    wid = request.POST["wid"]
    # 获取作品
    work, ret_code = get_work_by_id(wid)
    if ret_code != Error.OK:
        return error_response(ret_code)
    if work_is_mine(request, work) is False:
        return error_response(Error.NOT_YOUR_WORK)

    ret_code = delete_work(work)
    if ret_code != Error.OK:
        return error_response(ret_code)

    return response()

