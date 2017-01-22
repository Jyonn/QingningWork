import datetime
from Base.decorator import *
from Work.models import Work
from Comment.models import Comment
from Work.views import get_packed_work, get_work_by_id, work_is_mine


@require_POST
@require_login_reviewer
def get_related_lists(request):
    """
    审稿员获取
    1. related_not_reviewed 尚未审阅，且稿件状态为正在审阅的稿件
    2. related_received     已审并接收的稿件
    3. related_refused      已审并驳回的稿件
    4. related_upload       发布的稿件
    response
    {
        code: 0,
        msg: "ok",
        body: [{
            related_type: 和审稿员的关系1-4
            wid: 作品编号
            writer_name: 作者名称
            work_name: 作品名称
            create_time: 创建时间
            status: 稿件状态
            is_public: 是否公开
            is_delete: 是否被删除
            recv_num: 过审数
            refs_num: 驳回数
        },  {
            ...
        }]
    }
    """
    # 获取审稿员
    reviewer, user_type = get_user_from_session(request)
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)

    # 获取还未审阅的稿件列表
    works = Work.objects.filter(
        status=Work.STATUS_UNDER_REVIEW,  # 状态为接受审阅
        is_delete=False,  # 非删除稿件
    )
    return_list = []
    for work in works:
        try:
            # 如果存在评价，则属于审阅过的稿件
            Comment.objects.get(
                re_work=work,
                re_reviewer=reviewer,
                is_updated=False,
            )
        except:
            # 没有审阅过的稿件，加入返回列表
            return_list.append(get_packed_work(work, Reviewer.RELATED_NOT_REVIEWED))

    # 获取已审的稿件列表
    comments = Comment.objects.filter(
        re_reviewer=reviewer,
        is_updated=False
    )
    for comment in comments:
        if comment.result is True:
            # 审阅驳回的稿件
            return_list.append(get_packed_work(comment.re_work, Reviewer.RELATED_RECEIVED))
        else:
            # 审阅通过的稿件
            return_list.append(get_packed_work(comment.re_work, Reviewer.RELATED_REFUSED))

    # 获取发布的稿件列表
    works = Work.objects.filter(
        re_reviewer=reviewer,
        is_delete=False,
    )
    for work in works:
        return_list.append(get_packed_work(work, Reviewer.RELATED_UPLOAD))

    return response(body=return_list)


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
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)

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
            work_detail = dict(
                wid=work.pk,
                writer_name=work.writer_name,
                work_name=work.work_name,
                create_time=get_readable_time_string(work.create_time),
            )
            if work.re_writer is not None:
                work_detail["re_avatar"] = work.re_writer.avatar
            else:
                work_detail["re_avatar"] = work.re_reviewer.avatar
            return_list.append(work_detail)
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
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)

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
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)

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
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)
    if len(content) > 400:
        return error_response(Error.COMMENT_TOO_LONG)
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
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)

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


def get_rank(reviewer, order_by):
    reviewers = Reviewer.objects.filter(is_frozen=False).order_by(order_by)
    attr = order_by
    if order_by[0] == '-':
        attr = attr[1:]
    rank = 0
    for ret_reviewer in reviewers:
        rank += 1
        if getattr(ret_reviewer, attr) == getattr(reviewer, attr):
            break
    return rank


@require_POST
@require_login_reviewer
def info(request):
    """
    获取审稿员基本信息
    response
    {
        nickname: 笔名/昵称
        avatar: 头像地址
        total_review: 已审作品数目
        total_received: 通过作品数目
        total_refused: 驳回作品数目
        total_upload: 发布作品数目
        total_upload_rank: 发布作品排名
        login_times: 登录次数
        last_ipv4: 上次登录地址
        last_login: 上次登录时间
    }
    """
    reviewer, user_type = get_user_from_session(request)
    if reviewer is None:
        return error_response(Error.LOGIN_AGAIN)
    total_upload_rank = get_rank(reviewer, "-total_upload")
    total_review_rank = get_rank(reviewer, "-total_review")

    last_login_str = "第一次登录" if reviewer.last_login is None else reviewer.last_login.strftime("%Y-%m-%d %H:%M:%S")
    ip_str = "第一次登录" if reviewer.last_ipv4 is None else get_address_by_ip_via_sina(reviewer.last_ipv4)

    return_dict = dict(
        nickname=reviewer.nickname,
        avatar=reviewer.avatar,
        total_review=reviewer.total_review,
        total_received=reviewer.total_received,
        total_refused=reviewer.total_refused,
        total_upload=reviewer.total_upload,
        total_upload_rank=total_upload_rank,
        total_review_rank=total_review_rank,
        login_times=reviewer.login_times,
        last_ipv4=ip_str,
        last_login=last_login_str,
    )

    return response(body=return_dict)


@require_POST
@require_json
@require_params(["wid", "writer_username"])
@require_login_reviewer
def bind_writer(request):
    wid = request.POST["wid"]
    writer_username = request.POST["writer_username"]
    work, ret_code = get_work_by_id(wid)
    if ret_code != Error.OK:
        return error_response(ret_code)
    if work_is_mine(request, work) is False:
        return error_response(Error.NOT_YOUR_WORK)
    try:
        writer = Writer.objects.get(username=writer_username)
        if writer.is_frozen:
            return error_response(Error.FROZEN_USER)
    except:
        return error_response(Error.NOT_FOUND_USERNAME)
    work.re_writer = writer
    work.save()

    return response()
