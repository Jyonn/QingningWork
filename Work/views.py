from pydoc import html

from Base.decorator import *
from Comment.models import Comment
from QingningWork.settings import WORK_URL
from Work.models import Work


@require_POST
@require_json
@require_params(["wid"])
@require_login
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
    }
    """
    wid = request.POST["wid"]

    try:
        work = Work.objects.get(pk=wid)
    except:
        return error_response(Error.NOT_FOUND_WORK_ID)
    if work.is_delete is True:
        return error_response(Error.WORK_HAS_DELETED)
    if work.is_public is False:
        return error_response(Error.WORK_IS_PRIVATE)

    work_detail = dict(
        wid=work.pk,
        writer_name=work.writer_name,
        work_name=work.work_name,
        create_time=work.create_time.strftime("%Y-%m-%d %H:%M:%S"),
        status=work.status,
        fee=work.fee,
        work_type=work.work_type,
    )
    if work.re_writer is not None:
        work_detail["re_writer_id"] = work.re_writer.pk
        work_detail["re_reviewer_id"] = None
    else:
        work_detail["re_reviewer_id"] = work.re_reviewer.pk
        work_detail["re_writer_id"] = None
    if work.work_type == Work.WORK_TYPE_TEXT:
        file_path = WORK_URL + work.work_store
        with open(file_path, "rb+") as f:
            content = f.read().decode()
            content = html.escape(content)
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
@require_login
def get_work_comments(request):
    """
    获取作品的所有最新评论
    """
    wid = request.POST["wid"]
    try:
        work = Work.objects.get(pk=wid)
    except:
        return error_response(Error.NOT_FOUND_WORK_ID)
    if work.is_delete is True:
        return error_response(Error.WORK_HAS_DELETED)
    if work.is_public is False:
        return error_response(Error.WORK_IS_PRIVATE)

    comment_list = []
    comments = Comment.objects.filter(
        re_work=work,
        is_updated=False,
    )
    for comment in comments:
        comment_list.append(dict(
            rid=comment.re_reviewer.pk,
            reviewer_name=comment.re_reviewer.nickname,
            content=comment.content,
            result=comment.result,
            comment_time=comment.comment_time,
        ))

    return response(body=comment_list)
