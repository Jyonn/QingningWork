# coding=utf-8
# import datetime
from django.shortcuts import render

from AbstractUser.front_views import get_packed_work_comment
from BaseFunc.decorator import *
from Comment.models import Comment, WriterComment, WriterLike
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
        return None, Error.NOT_FOUND_WORK
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
        dist_str = str(int(dist / 60)) + '分钟前'
    elif dist < 60 * 60 * 24:
        dist_str = str(int(dist / 60 / 60)) + '小时前'
    elif dist < 60 * 60 * 24 * 30:
        dist_str = str(int(dist / 60 / 60 / 24)) + '天前'
    elif dist < 60 * 60 * 24 * 365:
        dist_str = str(int(dist / 60 / 60 / 24 / 30)) + '个月前'
    else:
        dist_str = str(int(dist / 60 / 60 / 24 / 365)) + '年前'

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
        return error_response(Error.NOT_FOUND_WORK)
    if not work_belongs(last_work, o_user):
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
@require_params(['work_id'])
@require_login
def delete(request):
    work_id = request.POST['work_id']
    o_user = get_user_from_session(request)

    try:
        work = Work.objects.get(pk=work_id, is_delete=False)
    except:
        return error_response(Error.NOT_FOUND_WORK)

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

    old_html_id = None
    new_comment = None

    if o_user.user_type == AbstractUser.TYPE_WRITER:
        if len(content) < 1:
            return error_response(Error.COMMENT_ERROR)
        writer = Writer.objects.get(pk=o_user.user_id)
        o_writer_comment = WriterComment.create(work, writer, content)
        new_comment = o_writer_comment
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
            old_html_id = o_comment.get_html_id()
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

        o_comment = Comment.create(work, reviewer, content, passed)
        new_comment = o_comment
    new_comment_dict = get_packed_work_comment(o_user, new_comment, o_user.user_type == AbstractUser.TYPE_REVIEWER)
    new_html = render(request, 'v2/comment-item.html', dict(comment=new_comment_dict)).content.decode('utf-8')
    return response(body=dict(old_html_id=old_html_id, new_html=new_html, new_html_id=new_comment.get_html_id()))


@require_POST
@require_json
@require_params(['like', 'work_id'])
@require_login
def like(request):
    result = request.POST['like'] == 'true'
    work_id = request.POST['work_id']
    o_user = get_user_from_session(request)

    if o_user.is_frozen:
        return error_response(Error.FROZEN_USER)

    try:
        work = Work.objects.get(pk=work_id, is_delete=False, is_public=True)
    except:
        return error_response(Error.NOT_FOUND_WORK)

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
    if o_user.is_frozen:
        return error_response(Error.FROZEN_USER)
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


@require_POST
@require_json
@require_params(['work_id', 'be_public'])
@require_login
def set_privilege(request):
    work_id = request.POST['work_id']
    be_public = request.POST['be_public'] == 'true'
    o_user = get_user_from_session(request)
    try:
        work = Work.objects.get(pk=work_id, is_delete=False)
    except:
        return error_response(Error.NOT_FOUND_WORK)
    if not work_belongs(work, o_user):
        return error_response(Error.NOT_YOUR_WORK)

    work.is_public = be_public
    work.save()

    return response()
