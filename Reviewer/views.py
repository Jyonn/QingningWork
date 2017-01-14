from QingningWork.settings import WORK_URL

import datetime
from Base.decorator import *
from Work.models import Work
from Comment.models import Comment
# from bs4 import BeautifulSoup
# import HTMLParser
# from pydoc import html
# import cgi


@require_POST
@require_json
@require_params(["work_type", "work_name", "writer_name", "content"])
@require_login_reviewer
def upload_work(request):
    """
    审稿员上传稿件
    request
    {
        work_type: 作品类型，只能为 WORK_TYPE_FILE 或 WORK_TYPE_TEXT
        work_name: 作品名称
        writer_name: 作者名称
        content: 作品正文，当 work_type 为 WORK_TYPE_TEXT 时有效
        file: 上传的作品，当 work_type 为 WORK_TYPE_FILE 时有效
    }
    """
    work_type = request.POST["work_type"]  # 作品类型（WORK_TYPE_FILE文件上传; WORK_TYPE_TEXT文本上传）
    work_name = request.POST["work_name"]  # 作品名称，指题目
    writer_name = request.POST["writer_name"]  # 作者名称
    content = request.POST["content"]
    reviewer, user_type = get_user_from_session(request)

    try:
        work_type = int(work_type)
    except:
        return error_response(Error.NOT_FOUND_WORK_TYPE)
    if work_type not in [Work.WORK_TYPE_FILE, Work.WORK_TYPE_TEXT]:
        # 不存在的作品类型
        return error_response(Error.NOT_FOUND_WORK_TYPE)

    if work_type == Work.WORK_TYPE_FILE:
        # 如果是文件，获取文件扩展名
        if request.FILES.get("file") is None:
            return error_response(Error.NOT_FOUND_FILE)
        str_name = request.FILES.get("file").name
        ext_name = "" if str_name.find(".") == -1 else "." + str_name.split(".")[-1]
    else:
        # 如果是文本，默认扩展名为txt
        ext_name = ".txt"

    moment = datetime.datetime.now()
    create_time = moment.strftime("%Y-%m-%d %H:%M:%S")
    head_filename = moment.strftime("%Y%m%d_%H%M%S_")
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
        # 保存文本文件
        with open(file_path, "wb+") as f:
            f.write(bytes(content, encoding="utf8"))
            f.close()

    # 存入数据库
    Work.create(
        re_reviewer=reviewer,
        writer_name=writer_name,
        work_name=work_name,
        work_store=filename,
        work_type=work_type,
        is_public=True,
        status=Work.STATUS_UNDER_REVIEW,
        create_time=create_time,
    )

    reviewer.total_upload += 1
    reviewer.save()

    return response()


@require_POST
@require_login_reviewer
def get_not_reviewed_list(request):
    """
    审稿员获取尚未审阅，且稿件状态为正在审阅的稿件
    response
    {
        code: 0,
        msg: "ok",
        body: [{
            wid: 作品编号
            writer_name: 作者名称
            work_name: 作品名称
            create_time: 创建时间
        },  {
            ...
        }]
    }
    """
    reviewer, user_type = get_user_from_session(request)
    works = Work.objects.filter(
        status=Work.STATUS_UNDER_REVIEW,
        is_delete=False,
    )
    return_list = []
    for work in works:
        comment_work = Comment.objects.filter(
            re_work=work,
            re_reviewer=reviewer,
            is_updated=False,
        )
        if comment_work.count() == 0:
            return_list.append(dict(
                wid=work.pk,
                writer_name=work.writer_name,
                work_name=work.work_name,
                create_time=work.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            ))
    return response(body=return_list)


@require_POST
@require_login_reviewer
def get_reviewed_list(request):
    """
    审稿员获取已审阅的稿件
    response
    {
        code: 0,
        msg: "ok",
        body: [{
            wid: 作品编号
            writer_name: 作者名称
            work_name: 作品名称
            create_time: 创建时间
            status: 作品状态
            is_public: 是否公开
            is_delete: 是否被删除
            result: 审阅结果
            comment_time: 审阅时间
        },  {
            ...
        }]
    }
    """
    reviewer, user_type = get_user_from_session(request)

    return_list = []  # 返回列表
    # 获取已审阅稿件列表
    comment_works = Comment.objects.filter(
        re_reviewer=reviewer,
        is_updated=False,
    )
    for comment_work in comment_works:
        work = comment_work.re_work
        # 提取关键字段
        return_list.append(dict(
            wid=work.pk,
            writer_name=work.writer_name,
            work_name=work.work_name,
            create_time=work.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            status=work.status,
            is_public=work.is_public,
            is_delete=work.is_delete,
            result=comment_work.result,
            comment_time=comment_work.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
        ))
    return response(body=return_list)


@require_POST
@require_json
@require_params(["wid"])
@require_login_reviewer
def get_reviewed_work(request):
    """
    审稿员获取他对某条作品的所有评论
    """
    wid = request.POST["wid"]
    reviewer, user_type = get_user_from_session(request)

    try:
        work = Work.objects.get(pk=wid)
    except:
        return error_response(Error.NOT_FOUND_WORK_ID)

    return_dict = dict(
        work=dict(
            wid=work.pk,
            writer_name=work.writer_name,
            work_name=work.work_name,
            create_time=work.create_time.strftime("%Y-%m-%d %H:%M:%S"),
            status=work.status,
            is_public=work.is_public,
            is_delete=work.is_delete,
        )
    )
    comment_list = []  # 返回列表
    # 获取已审阅稿件列表
    comment_works = Comment.objects.filter(
        re_work=work,
        re_reviewer=reviewer,
    )
    for comment_work in comment_works:
        # 提取关键字段
        comment_list.append(dict(
            is_updated=comment_work.is_updated,
            comment=comment_work.content,
            result=comment_work.result,
            comment_time=comment_work.comment_time.strftime("%Y-%m-%d %H:%M:%S"),
        ))
    return_dict["comments"] = comment_list
    return response(body=return_dict)


@require_POST
@require_json
@require_params(["wid", "content", "result"])
@require_login_reviewer
def review_work(request):
    """
    审稿员审阅稿件并上传结果
    request
    {
        wid: 作品编号
        content: 审阅评价
        result: 审阅结果，为 True 或 False
    }
    """
    wid = request.POST["wid"]
    content = request.POST["content"]
    result = True if request.POST["result"] is True else False
    reviewer, user_type = get_user_from_session(request)

    try:
        work = Work.objects.get(pk=wid)
    except:
        return error_response(Error.NOT_FOUND_WORK_ID)
    if work.status != Work.STATUS_UNDER_REVIEW:  # 不在审阅状态，非法获取
        return error_response(Error.NOT_UNDER_REVIEW)
    if work.is_delete:
        return error_response(Error.WORK_HAS_DELETED)
    writer = work.re_writer

    # 更新原评论（不销毁）
    try:
        comment = Comment.objects.get(
            re_work=work,
            re_reviewer=reviewer,
            is_updated=False,
        )
        comment.is_updated = True  # 原评论被更新标记
        comment.save()
        # 若评价结果不同，更新审稿员和作者数据
        if comment.result != result:
            # 更新审稿员
            if result is True:
                reviewer.total_received += 1  # 审稿员接收量+1
                reviewer.total_refused -= 1  # 审稿员驳回量-1
            else:
                reviewer.total_received -= 1  # 审稿员接收量-1
                reviewer.total_refused += 1  # 审稿员驳回量+1
            reviewer.save()

            # 更新作者
            if writer is not None:
                if result is True:
                    writer.total_received += 1  # 作者接收量+1
                    writer.total_refused -= 1  # 作者驳回量-1
                else:
                    writer.total_received -= 1  # 作者接收量-1
                    writer.total_refused += 1  # 作者驳回量+1
                writer.save()
    except:
        # 审稿员第一次评价
        reviewer.total_review += 1  # 审稿员审稿总数+1
        if result is True:
            reviewer.total_received += 1  # 审稿员接收量+1
        else:
            reviewer.total_refused += 1  # 审稿员驳回量-1
        reviewer.save()
        # 更新作者
        if writer is not None:
            if result is True:
                writer.total_received += 1
            else:
                writer.total_refused += 1
        writer.save()

    # 创建新评论
    moment = datetime.datetime.now()
    comment_time = moment.strftime("%Y-%m-%d %H:%M:%S")
    Comment.create(
        re_work=work,
        re_reviewer=reviewer,
        content=content,
        result=result,
        comment_time=comment_time,
        is_updated=False,
    )

    return response()


@require_POST
@require_json
@require_params(["wid"])
@require_login_reviewer
def delete_work(request):
    """
    审稿员删除他上传的某条作品
    request
    {
        wid: 作品编号
    }
    """
    wid = request.POST["wid"]
    reviewer, user_type = get_user_from_session(request)

    try:
        work = Work.objects.get(pk=wid, re_reviewer=reviewer)
    except:
        return error_response(Error.NOT_YOUR_WORK)
    if work.is_delete:  # 已被删除
        return error_response(Error.WORK_HAS_DELETED)

    # 更新作品为已删除
    work.is_delete = True
    work.save()

    return response()
