from django.shortcuts import render

from AbstractUser.models import AbstractUser
from BaseFunc.base import get_readable_time_string, get_user_from_session
from Comment.models import WriterLike, Comment, WriterComment
from Reviewer.models import Reviewer
from Timeline.models import Timeline
from Writer.models import Writer, Follow


def get_user_info(o_user):
    if o_user is None:
        return dict(
            is_login=False,
            is_reviewer=False,
            is_writer=False,
        )
    else:
        return dict(
            is_login=True,
            is_frozen=o_user.is_frozen,
            is_reviewer=o_user.user_type == AbstractUser.TYPE_REVIEWER,
            is_writer=o_user.user_type == AbstractUser.TYPE_WRITER,
            avatar=o_user.get_avatar(),
            nickname=o_user.get_nickname(),
            user_home='/v2/user/' + str(o_user.uid) + '/' + str(o_user.pk),
        )


def get_user_card(o_user, home_click=True):
    return dict(
        nickname=o_user.get_nickname(),
        introduce=o_user.get_introduce(),
        avatar=o_user.get_avatar(),
        is_reviewer=o_user.user_type == AbstractUser.TYPE_REVIEWER,
        home_link='/v2/user/' + str(o_user.pk) + '/' + str(o_user.user_id),
        home_click=home_click,
    )


def get_packed_work_thumbs(o_user, work, length=None):
    reviewer_likes = Comment.objects.filter(re_work=work, is_updated=False, result=True)
    writer_likes = WriterLike.objects.filter(re_work=work, is_deleted=False)
    thumb_list = []
    for thumb in reviewer_likes:
        if thumb.re_reviewer == o_user and length is not None:
            continue
        thumb_list.append(get_user_card(thumb.re_reviewer))
    for thumb in writer_likes[:length]:
        if thumb.re_writer == o_user and length is not None:
            continue
        thumb_list.append(get_user_card(thumb.re_writer))
    total_likes = len(reviewer_likes) + len(writer_likes)
    return thumb_list, total_likes


def get_packed_work_comments(o_user, work, length=None, show_self=False):
    reviewer_comments = Comment.objects.filter(re_work=work, is_updated=False)

    total_comments = 0
    comment_list = []
    comment_user_list = []
    comment_user_uid_list = []
    writer_comments = WriterComment.objects.filter(re_work=work, is_deleted=False)
    for comment in reviewer_comments:
        if comment.content is not None and len(comment.content) > 0:
            total_comments += 1
            if comment.re_reviewer == o_user and not show_self:
                continue
            comment_list.append(dict(
                avatar=comment.re_reviewer.get_avatar(),
                nickname=comment.re_reviewer.get_nickname(),
                time=get_readable_time_string(comment.comment_time),
                content=comment.content,
                is_reviewer=True,
                home_link='/v2/user/' + str(comment.re_reviewer.uid) + '/' + str(comment.re_reviewer.pk),
                is_mine=comment.re_reviewer == o_user,
            ))
            comment_user_list.append(comment.re_reviewer.get_nickname())

    total_comments += len(writer_comments)
    for comment in writer_comments[:length]:
        if comment.re_writer == o_user and not show_self:
            continue
        comment_list.append(dict(
            avatar=comment.re_writer.get_avatar(),
            nickname=comment.re_writer.get_nickname(),
            time=get_readable_time_string(comment.create_time),
            content=comment.content,
            is_reviewer=False,
            home_link='/v2/user/' + str(comment.re_writer.uid) + '/' + str(comment.re_writer.pk),
            is_mine=comment.re_writer == o_user,
        ))
        if comment.re_writer.uid not in comment_user_uid_list:
            comment_user_uid_list.append(comment.re_writer.uid)
            comment_user_list.append(comment.re_writer.get_nickname())

    comment_str = '、'
    comment_str = comment_str.join(comment_user_list)
    return comment_list, total_comments, comment_str


def get_interact_info(o_user, work):
    """
    获取用户和作品的互动关系
    :param o_user: 不能是AbstractUser类，必须为Reviewer或Writer
    :param work: 作品类
    :return: 互动字典
    """
    if o_user is None:
        return dict(
            thumb=False,
            has_comment=False,
        )
    thumb, has_comment = False, False
    comment = ''
    if o_user.user_type == AbstractUser.TYPE_REVIEWER:
        try:
            o_comment = Comment.objects.get(is_updated=False, re_reviewer=o_user, re_work=work)
            has_comment = o_comment.content not in [None, '']
            thumb = o_comment.result
            comment = o_comment.content
        except:
            pass
    if o_user.user_type == AbstractUser.TYPE_WRITER:
        try:
            o_thumb = WriterLike.objects.get(re_work=work, re_writer=o_user)
            thumb = not o_thumb.is_deleted
        except:
            pass
        try:
            o_comment = WriterComment.objects.filter(re_work=work, re_writer=o_user, is_deleted=False)
            has_comment = len(o_comment) > 0
        except:
            pass
    return dict(
        thumb=thumb,
        has_comment=has_comment,
        comment=comment if comment is not None else '',
    )


def get_packed_event(o_user,
                     event,
                     full_content=True,
                     show_self=False,
                     ):
    """
    获取事件（时间线）信息字典
    :param show_self: comment中是否展示我
    :param o_user: 不能是AbstractUser类，必须为Reviewer或Writer
    :param event: TimeLine类
    :param full_content: 展示全部内容
    :return:
    """
    re_work = event.related_work
    owner = event.owner

    thumb_list, total_thumbs = get_packed_work_thumbs(o_user, re_work, 5)
    thumb_str = ''
    for thumb in thumb_list[:-1]:
        thumb_str += thumb['nickname'] + '、'
    if len(thumb_list) > 0:
        thumb_str += thumb_list[-1]['nickname']

    comment_list, total_comments, comment_str = get_packed_work_comments(o_user, re_work, length=5, show_self=show_self)
    event_info = dict(
        work=dict(
            title=re_work.work_name if re_work.work_name is not None and len(re_work.work_name) > 0 else '未命名',
            writer=re_work.writer_name,
            version=re_work.version_num,
            content=re_work.content if full_content else re_work.content[:120] + '……',
            visit=re_work.total_visit,
            thumbs=total_thumbs,
            thumb_list=thumb_list,
            thumb_str=thumb_str,
            comments=total_comments,
            comment_list=comment_list,
            comment_str=comment_str,
        ),
        info=dict(
            type=dict(
                create=event.type == Timeline.TYPE_CREATE_WORK,
                modify=event.type == Timeline.TYPE_MODIFY_WORK,
                repost=event.type == Timeline.TYPE_REPOST_WORK,
            ),
            intro='' if owner.introduce is None else owner.introduce,
            time=get_readable_time_string(event.create_time),
            event_owner_home='/v2/user/' + str(owner.uid) + '/' + str(owner.pk),
            event_owner_avatar=owner.get_avatar(),
            event_owner_nickname=owner.get_nickname(),
            work_owner_avatar=re_work.re_writer.get_avatar() if re_work.re_writer is not None
            else re_work.re_reviewer.get_avatar(),
            event_link='/v2/event/' + str(owner.pk) + '/' + str(re_work.pk) + '/' + str(event.pk),
            thumb_link='/v2/thumbs/' + str(owner.pk) + '/' + str(re_work.pk) + '/' + str(event.pk),
            comment_link='/v2/comments/' + str(owner.pk) + '/' + str(re_work.pk) + '/' + str(event.pk),
            event_id=event.pk,
            work_id=re_work.pk,
            owner_id=owner.pk,
        ),
        interact=get_interact_info(o_user, re_work),
    )
    return event_info


def user(request):
    return render(request, 'v2/user-info.html')


def thumb_page(request, owner_id, work_id, event_id):
    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
        work = event.related_work
    except:
        return render(request, 'v2/login.html')

    o_user = get_user_from_session(request)

    thumb_list, total_thumbs = get_packed_work_thumbs(o_user, work)
    return render(request, 'v2/user-card-list.html', dict(
        thumb_list=thumb_list,
        title=str(total_thumbs) + '人觉得很赞',
    ))


def comment_page(request, owner_id, work_id, event_id):
    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
        work = event.related_work
    except:
        return render(request, 'v2/login.html')

    o_user = get_user_from_session(request)

    comment_list, total_comments, comment_str = get_packed_work_comments(o_user, work, length=None, show_self=True)
    # print(comment_list)
    return render(request, 'v2/comment-list.html', dict(comment_list=comment_list, count=total_comments))


def event_page(request, owner_id, work_id, event_id):
    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, owner__pk=owner_id)
    except:
        return render(request, 'v2/login.html')

    re_work = event.related_work
    re_work.total_visit += 1
    re_work.save()

    o_user = get_user_from_session(request)

    event_info = get_packed_event(
        o_user,
        event,
        full_content=True,
        show_self=True,
    )
    page_info = dict(
        thumb_click=True,
        content_click=False,
        abstract_comment=False,
        list_comment=True,
        show_comment_icon=True,
    )
    return render(request, "v2/event.html",
                  dict(event=event_info, user_info=get_user_info(o_user), page_info=page_info))


def event_list_packer(request, events):
    o_user = get_user_from_session(request)

    event_list = []
    for event in events:
        event_list.append(get_packed_event(
            o_user,
            event,
            full_content=False,
            show_self=False,
        ))
    page_info = dict(
        thumb_click=False,
        content_click=True,
        abstract_comment=True,
        list_comment=False,
        show_comment_icon=False,
    )

    return dict(
        event_list=event_list,
        user_info=get_user_info(o_user),
        page_info=page_info
    )


def center(request):
    events = Timeline.objects.filter(
        is_delete=False,
        related_work__is_updated=False,
        related_work__is_delete=False,
        related_work__is_public=True,
    ).order_by('-pk')
    return render(request, "v2/center.html", event_list_packer(request, events))


def require_review(request):
    o_user = get_user_from_session(request)
    if o_user.user_type != AbstractUser.TYPE_REVIEWER:
        return render(request, 'v2/login.html')
    events = Timeline.objects.filter(
        is_delete=False,
        type__in=(Timeline.TYPE_MODIFY_WORK, Timeline.TYPE_CREATE_WORK),
        related_work__is_delete=False,
        related_work__is_updated=False,
        related_work__is_public=True,
    )
    filter_events = []
    for event in events:
        try:
            Comment.objects.get(is_updated=False, re_reviewer=o_user, re_work=event.related_work)
        except:
            filter_events.append(event)
    return render(request, 'v2/center.html', event_list_packer(request, filter_events))


def follow_events(request):
    o_user = get_user_from_session(request)
    if o_user.user_type != AbstractUser.TYPE_WRITER:
        return render(request, 'v2/login.html')
    follows = Follow.objects.filter(follower=o_user, is_delete=False)
    followees = []
    for follow in follows:
        followees.append(follow.followee)
    events = Timeline.objects.filter(
        owner__in=followees,
        is_delete=False,
        related_work__is_public=True,
        related_work__is_updated=False,
        related_work__is_delete=False,
    )
    return render(request, 'v2/center.html', event_list_packer(request, events))


def user_home(request, user_id, role_id):
    try:
        o_visit_user = AbstractUser.objects.get(pk=user_id, is_frozen=False, user_id=role_id)
    except:
        return render(request, 'v2/login.html')
    card_info = get_user_card(o_visit_user, home_click=False)
    event_list = []

    o_user = get_user_from_session(request)

    if o_visit_user.user_type == AbstractUser.TYPE_WRITER:
        writer = Writer.objects.get(wid=o_visit_user.user_id)
        events = Timeline.objects.filter(
            is_delete=False,
            owner=writer,
            related_work__is_updated=False,
            related_work__is_delete=False,
            related_work__is_public=True,
        ).order_by('-pk')[:20]
        for event in events:
            event_list.append(get_packed_event(
                o_user,
                event,
                full_content=False,
                show_self=False,
            ))
        work_info = dict(
            total_works=writer.total_works,
            total_follow=writer.total_follow,
            total_followed=writer.total_followed,
        )
    else:
        reviewer = Reviewer.objects.get(rid=o_visit_user.user_id)
        work_info = dict(
            total_upload=reviewer.total_upload,
            total_review=reviewer.total_review,
            total_likes=reviewer.total_likes,
        )
    page_info = dict(
        thumb_click=False,
        content_click=True,
        abstract_comment=True,
        list_comment=False,
        show_comment_icon=False,
    )
    return render(request, 'v2/user-info.html', dict(
        event_list=event_list,
        card_info=card_info,
        work_info=work_info,
        page_info=page_info,
        user_info=get_user_info(o_user),
    ))


def upload_work(request):
    o_user = get_user_from_session(request)
    return render(request, 'v2/work-edit.html', dict(
        user_info=get_user_info(o_user),
        page_info=dict(
            is_create=True,
            is_modify=False,
        ),
    ))


def modify_work(request):
    o_user = get_user_from_session(request)
    if o_user is None:
        return render(request, 'v2/login.html')



def login_v2(request):
    return render(request, "v2/login.html")


def login(request):
    return render(request, "login.html")


def info(request):
    return render(request, "info.html")
