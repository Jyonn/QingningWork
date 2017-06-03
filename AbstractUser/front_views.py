from django.shortcuts import render

from AbstractUser.models import AbstractUser
from BaseFunc.base import get_readable_time_string
from Comment.models import WriterLike, Comment, WriterComment
from Reviewer.models import Reviewer
from Timeline.models import Timeline
from Work.models import Work
from Writer.models import Writer


def get_user_card(o_user):
    return dict(
        nickname=o_user.get_nickname(),
        introduce=o_user.get_introduce(),
        avatar=o_user.get_avatar(),
        is_reviewer=o_user.user_type == AbstractUser.TYPE_REVIEWER,
    )


def get_packed_work_thumbs(work, length=None):
    reviewer_likes = Comment.objects.filter(re_work=work, is_updated=False, result=True)
    writer_likes = WriterLike.objects.filter(re_work=work, is_deleted=False)
    thumb_list = []
    for thumb in reviewer_likes:
        thumb_list.append(get_user_card(thumb.re_reviewer))
    for thumb in writer_likes[:length]:
        thumb_list.append(get_user_card(thumb.re_writer))
    total_likes = len(reviewer_likes) + len(writer_likes)
    return thumb_list, total_likes


def get_packed_work_comments(work, length=None):
    reviewer_comments = Comment.objects.filter(re_work=work, is_updated=False)

    total_comments = 0
    comment_list = []
    writer_comments = WriterComment.objects.filter(re_work=work, is_deleted=False)
    for comment in reviewer_comments:
        if len(comment.content) > 0:
            total_comments += 1
            comment_list.append(dict(
                avatar=comment.re_reviewer.get_avatar(),
                nickname=comment.re_reviewer.nickname,
                time=get_readable_time_string(comment.comment_time),
                content=comment.content,
                is_reviewer=True,
            ))
    total_comments += len(writer_comments)
    for comment in writer_comments[:length]:
        comment_list.append(dict(
            avatar=comment.re_writer.get_avatar(),
            nickname=comment.re_writer.nickname,
            time=get_readable_time_string(comment.create_time),
            content=comment.content,
            is_reviewer=False,
        ))
    return comment_list, total_comments


def get_packed_event(event, need_comment=True, full_content=True):
    re_work = event.related_work
    re_writer = event.related_writer

    like_list, total_likes = get_packed_work_thumbs(re_work, 5)

    if need_comment:
        comment_list, total_comments = get_packed_work_comments(re_work, 5)
    else:
        comment_list, total_comments = [], 0

    event_info = dict(
        work=dict(
            title=re_work.work_name if re_work.work_name is not None and len(re_work.work_name) > 0 else '未命名',
            writer=re_work.writer_name,
            version=re_work.version_num,
            content=re_work.content if full_content else re_work.content[:120] + '……',
            visit=re_work.total_visit,
            thumbs=total_likes,
            thumb_list=like_list,
            comments=total_comments,
            comment_list=comment_list,
        ),
        info=dict(
            type=dict(
                create=event.type == Timeline.TYPE_CREATE_WORK,
                modify=event.type == Timeline.TYPE_MODIFY_WORK,
                repost=event.type == Timeline.TYPE_REPOST_WORK,
            ),
            intro='' if re_writer.introduce is None else re_writer.introduce,
            time=get_readable_time_string(event.create_time),
            event_owner_avatar=re_writer.get_avatar(),
            event_owner_nickname=re_writer.nickname,
            event_owner_id=re_writer.pk,
            work_owner_avatar=re_work.re_writer.get_avatar() if re_work.re_writer is not None else re_work.re_reviewer.get_avatar(),
        )
    )
    return event_info


def user(request):
    return render(request, 'v2/user-info.html')


def thumb_page(request, work_id):
    try:
        work = Work.objects.get(pk=work_id, is_delete=False, is_public=True)
    except:
        return render(request, 'v2/login.html')
    thumb_list, total_thumbs = get_packed_work_thumbs(work)
    return render(request, 'v2/user-card-list.html', dict(
        thumb_list=thumb_list,
        title=str(total_thumbs)+'人觉得很赞',
    ))


def comment_page(request, work_id):
    try:
        work = Work.objects.get(pk=work_id, is_delete=False, is_public=True)
    except:
        return render(request, 'v2/login.html')
    comment_list, total_comments = get_packed_work_comments(work)
    return render(request, 'v2/comment-list.html', dict(comment_list=comment_list, count=total_comments))


def work_page(request, writer_id, work_id, event_id):
    try:
        event = Timeline.objects.get(pk=event_id, related_work__pk=work_id, related_writer__pk=writer_id)
    except:
        return render(request, 'v2/login.html')

    re_work = event.related_work
    re_work.total_visit += 1
    re_work.save()

    event_info = get_packed_event(event, need_comment=True, full_content=True)
    # print(event_info)
    return render(request, "v2/work.html", dict(event=event_info))


def center(request):
    events = Timeline.objects.filter(
        is_delete=False,
        related_work__is_updated=False,
        related_work__is_delete=False,
        related_work__is_public=True,
    ).order_by('-pk')[:20]
    event_list = []
    for event in events:
        event_list.append(get_packed_event(event, need_comment=False, full_content=False))
    return render(request, "v2/center.html", dict(event_list=event_list))


def user_home(request, user_id):
    try:
        o_user = AbstractUser.objects.get(pk=user_id, is_frozen=False)
    except:
        return render(request, 'v2/login.html')
    card_info = get_user_card(o_user)
    # print(card_info)
    event_list = []

    if o_user.user_type == AbstractUser.TYPE_WRITER:
        writer = Writer.objects.get(wid=o_user.user_id)
        events = Timeline.objects.filter(
            is_delete=False,
            related_writer=writer,
            related_work__is_updated=False,
            related_work__is_delete=False,
            related_work__is_public=True,
        ).order_by('-pk')[:20]
        for event in events:
            event_list.append(get_packed_event(event, need_comment=False, full_content=False))
        work_info = dict(
            total_works=writer.total_works,
            total_follow=writer.total_follow,
            total_followed=writer.total_followed,
        )
    else:
        reviewer = Reviewer.objects.get(rid=o_user.user_id)
        work_info = dict(
            total_upload=reviewer.total_upload,
            total_review=reviewer.total_review,
            total_likes=reviewer.total_likes,
        )
    return render(request, 'v2/user-info.html', dict(
        event_list=event_list,
        card_info=card_info,
        work_info=work_info,
    ))


def login_v2(request):
    return render(request, "v2/login.html")


def login(request):
    return render(request, "login.html")


def info(request):
    return render(request, "info.html")
