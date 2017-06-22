# coding=utf-8
# import datetime

from BaseFunc.decorator import *
from Comment.models import Comment, WriterComment, WriterLike
from QingningWork.settings import WORK_URL
from Reviewer.models import Reviewer
from Timeline.models import Timeline
from Work.models import Work
from Writer.models import Writer


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
        dist_str = str(int(dist)) + '秒前'
    elif dist < 60 * 60:
        dist_str = str(int(dist/60)) + '分钟前'
    elif dist < 60 * 60 * 24:
        dist_str = str(int(dist/60/60)) + '小时前'
    elif dist < 60 * 60 * 24 * 30:
        dist_str = str(int(dist/60/60/24)) + '天前'
    elif dist < 60 * 60 * 24 * 365:
        dist_str = str(int(dist/60/60/24/30)) + '个月前'
    else:
        dist_str = str(int(dist/60/60/24/365)) + '年前'

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
        work_detail['re_avatar'] = work.re_writer.avatar
    else:
        work_detail['re_avatar'] = work.re_reviewer.avatar
    return work_detail


@require_POST
@require_json
@require_params(['wid'])
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
    wid = request.POST['wid']
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
        work_detail['re_writer_id'] = work.re_writer.pk
    if work.re_reviewer is not None:
        work_detail['re_reviewer_id'] = work.re_reviewer.pk

    work_detail['is_mine'] = work_is_mine(request, work)

    if work.is_public is False and work_detail['is_mine'] is False:
        return error_response(Error.WORK_IS_PRIVATE)

    file_path = WORK_URL + work.work_store
    with open(file_path, 'rb+') as f:
        content = f.read().decode()
        f.close()
    work_detail['content'] = content
    work_detail['url'] = None

    return response(body=work_detail)


@require_POST
@require_json
@require_params(['wid'])
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
    wid = request.POST['wid']
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
    for o_comment in comments:
        reviewer_comments = Comment.objects.filter(re_work=work, re_reviewer=o_comment.re_reviewer)
        comment_list.append(dict(
            rid=o_comment.re_reviewer.pk,
            nickname=o_comment.re_reviewer.nickname,
            avatar=o_comment.re_reviewer.avatar,
            content=o_comment.content,
            result=o_comment.result,
            comment_time=get_readable_time_string(o_comment.comment_time),
            times=reviewer_comments.count(),
        ))

    return response(body=comment_list)


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
    for o_comment in comments:
        # 恢复审稿员的审稿数
        if o_comment.result is True:
            o_comment.re_reviewer.total_received -= 1
        else:
            o_comment.re_reviewer.total_refused -= 1
        o_comment.re_reviewer.save()

    # 标记删除
    work.is_delete = True
    work.save()
    return Error.OK


@require_POST
@require_json
@require_params(['work_name', 'writer_name', 'content', 'is_public', 'motion'])
@require_login
def upload(request):
    """
    审稿员或作者上传稿件
    request
    {
        work_name: 作品名称
        writer_name: 作者名称
        content: 作品正文，当 work_type 为 WORK_TYPE_TEXT 时有效
        is_public: 是否公开，仅对writer有效
    }
    """
    work_name = request.POST['work_name']
    writer_name = request.POST['writer_name']
    content = request.POST['content']
    is_public = request.POST['is_public'] == 'true'
    motion = request.POST['motion']
    o_user = get_user_from_session(request)
    if o_user.user_type == AbstractUser.TYPE_REVIEWER and not is_public:
        return error_response(Error.REVIEWER_PUBLIC)
    pattern = r'^\s*$'
    if re.search(pattern, work_name) is not None:
        return error_response(Error.WORK_NAME_NONE)
    if re.search(pattern, writer_name) is not None:
        return error_response(Error.WRITER_NAME_NONE)
    if re.search(pattern, content) is not None:
        return error_response(Error.CONTENT_NONE)

    o_work = Work.create(o_user, work_name, writer_name, content, is_public, None)
    if o_work is None:
        return error_response(Error.WORK_SAVE_ERROR)
    o_event = Timeline.create(o_user, o_work, Timeline.TYPE_CREATE_WORK, motion=motion)
    return response(body=dict(
        event_id=o_event.pk,
        work_id=o_work.pk,
        owner_id=o_user.uid,
    ))


@require_POST
@require_json
@require_params(['work_name', 'writer_name', 'content', 'is_public', 'motion', 'work_id'])
@require_login
def modify(request):
    """
    修改作品（懒惰删除，保留备份）
    """
    work_name = request.POST['work_name']
    writer_name = request.POST['writer_name']
    content = request.POST['content']
    is_public = request.POST['is_public'] == 'true'
    motion = request.POST['motion']
    work_id = request.POST['work_id']
    o_user = get_user_from_session(request)
    if o_user.user_type == AbstractUser.TYPE_REVIEWER and not is_public:
        return error_response(Error.REVIEWER_PUBLIC)
    pattern = r'^\s*$'
    if re.search(pattern, work_name) is not None:
        return error_response(Error.WORK_NAME_NONE)
    if re.search(pattern, writer_name) is not None:
        return error_response(Error.WRITER_NAME_NONE)
    if re.search(pattern, content) is not None:
        return error_response(Error.CONTENT_NONE)
    try:
        last_work = Work.objects.get(pk=work_id, is_delete=False).newest_version_work
    except:
        return error_response(Error.NOT_YOUR_WORK)

    o_work = Work.create(o_user, work_name, writer_name, content, is_public, last_work)
    if o_work is None:
        return error_response(Error.WORK_SAVE_ERROR)
    o_event = Timeline.create(o_user, o_work, Timeline.TYPE_MODIFY_WORK, motion=motion)

    return response(body=dict(
        event_id=o_event.pk,
        work_id=o_work.pk,
        owner_id=o_user.uid,
    ))


@require_POST
@require_json
@require_params(['event_id', 'work_id', 'owner_id'])
@require_login
def delete(request):
    event_id = request.POST['event_id']
    work_id = request.POST['work_id']
    owner_id = request.POST['owner_id']
    o_user = get_user_from_session(request)

    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
        work = event.related_work
    except:
        return error_response(Error.NOT_FOUND_EVENT)

    if not work_belongs(work, o_user):
        return error_response(Error.NOT_YOUR_WORK)
    if work.status == Work.STATUS_CONFIRM_FEE:
        return error_response(Error.CAN_NOT_DELETE_CAUSE_CONFIRMED)

    work.is_delete = True
    work.save()

    return response()


@require_POST
@require_json
@require_params(['content', 'pass', 'event_id', 'work_id', 'owner_id'])
@require_login
def comment(request):
    content = request.POST['content']
    passed = request.POST['pass'] == 'true'
    event_id = request.POST['event_id']
    work_id = request.POST['work_id']
    owner_id = request.POST['owner_id']
    o_user = get_user_from_session(request)

    if o_user.is_frozen:
        return error_response(Error.FROZEN_USER)

    if len(content) > WriterComment.L['content']:
        return error_response(Error.COMMENT_ERROR)

    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
        work = event.related_work
    except:
        return error_response(Error.NOT_FOUND_EVENT)

    if o_user.user_type == AbstractUser.TYPE_WRITER:
        if len(content) < 1:
            return error_response(Error.COMMENT_ERROR)
        writer = Writer.objects.get(pk=o_user.user_id)
        WriterComment.create(work, writer, content)
    elif o_user.user_type == AbstractUser.TYPE_REVIEWER:
        reviewer = Reviewer.objects.get(pk=o_user.user_id)
        writer = work.re_writer
        try:
            o_comment = Comment.objects.get(
                re_work=work,
                re_reviewer=reviewer,
                is_updated=False,
            )
            o_comment.is_updated = True  # 原评论被更新标记
            o_comment.save()
            # 若评价结果不同，更新审稿员和作者数据
            if o_comment.result != passed:
                # 更新审稿员
                if passed:
                    reviewer.total_received += 1  # 审稿员接收量+1
                    reviewer.total_refused -= 1  # 审稿员驳回量-1
                else:
                    reviewer.total_received -= 1  # 审稿员接收量-1
                    reviewer.total_refused += 1  # 审稿员驳回量+1
                reviewer.save()

                # 更新作者
                if writer is not None:
                    if passed:
                        writer.total_received += 1  # 作者接收量+1
                        writer.total_refused -= 1  # 作者驳回量-1
                    else:
                        writer.total_received -= 1  # 作者接收量-1
                        writer.total_refused += 1  # 作者驳回量+1
                    writer.save()
        except:
            # 审稿员第一次评价
            reviewer.total_review += 1  # 审稿员审稿总数+1
            if passed:
                reviewer.total_received += 1  # 审稿员接收量+1
            else:
                reviewer.total_refused += 1  # 审稿员驳回量-1
            reviewer.save()
            # 更新作者
            if writer is not None:
                if passed:
                    writer.total_received += 1
                else:
                    writer.total_refused += 1
                writer.save()

        Comment.create(work, reviewer, content, passed)
    return response()


@require_POST
@require_json
@require_params(['like', 'event_id', 'work_id', 'owner_id'])
@require_login
def like(request):
    result = request.POST['like'] == 'true'
    event_id = request.POST['event_id']
    work_id = request.POST['work_id']
    owner_id = request.POST['owner_id']
    o_user = get_user_from_session(request)

    if o_user.is_frozen:
        return error_response(Error.FROZEN_USER)

    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
        work = event.related_work
    except:
        return error_response(Error.NOT_FOUND_EVENT)

    if o_user.user_type == AbstractUser.TYPE_WRITER:
        try:
            o = WriterLike.objects.get(re_writer=o_user, re_work=work)
            o.is_deleted = not result
            o.save()
        except:
            WriterLike.create(work, o_user, not result)
    if o_user.user_type == AbstractUser.TYPE_REVIEWER:
        try:
            o = Comment.objects.get(re_work=work, re_reviewer=o_user, is_updated=False)
            o.result = result
            o.save()
        except:
            Comment.create(work, o_user, None, result)
    return response()


@require_POST
@require_json
@require_params(['comment_id', 'work_id'])
@require_login
def comment_delete(request):
    comment_id = request.POST['comment_id']
    work_id = request.POST['work_id']
    o_user = get_user_from_session(request)
    if o_user.user_type != AbstractUser.TYPE_WRITER:
        return error_response(Error.REQUIRE_WRITER)
    try:
        o_comment = WriterComment.objects.get(
            pk=comment_id,
            re_work_id=work_id,
            re_writer=o_user,
        )
        o_comment.is_deleted = True
        o_comment.save()
    except:
        return error_response(Error.COMMENT_DELETE_ERROR)
    return response()
