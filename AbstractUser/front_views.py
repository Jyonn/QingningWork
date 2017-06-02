from django.shortcuts import render

from BaseFunc.base import get_readable_time_string
from Comment.models import WriterLike, Comment, WriterComment
from Timeline.models import Timeline


def user(request):
    return render(request, 'v2/comment-list.html')


def work(request):
    event = Timeline.objects.get(pk=70)
    re_work = event.related_work
    re_work.total_visit += 1
    re_work.save()
    re_writer = event.related_writer
    reviewer_comments = Comment.objects.filter(re_work=re_work, is_updated=False)
    reviewer_likes = reviewer_comments.filter(result=True)
    writer_likes = WriterLike.objects.filter(re_work=re_work, is_deleted=False)
    like_list = []
    for like in reviewer_likes:
        like_list.append(like.re_reviewer.nickname)
    for like in writer_likes[:5]:
        like_list.append(like.re_writer.nickname)

    comment_count = 0
    writer_comments = WriterComment.objects.filter(re_work=re_work, is_deleted=False)
    comment_list = []
    for comment in reviewer_comments:
        if len(comment.content) > 0:
            comment_count += 1
            comment_list.append(dict(
                avatar=comment.re_reviewer.get_avatar(),
                nickname=comment.re_reviewer.nickname,
                time=get_readable_time_string(comment.comment_time),
                content=comment.content,
                is_reviewer=True,
            ))
    comment_count += len(writer_comments)
    for comment in writer_comments[:5]:
        comment_list.append(dict(
            avatar=comment.re_writer.get_avatar(),
            nickname=comment.re_writer.nickname,
            time=get_readable_time_string(comment.create_time),
            content=comment.content,
            is_reviewer=False,
        ))

    event_info = dict(
        work=dict(
            title=re_work.work_name if re_work.work_name is not None and len(re_work.work_name) > 0 else '未命名',
            writer=re_work.writer_name,
            version=re_work.version_num,
            content=re_work.content,
            visit=re_work.total_visit,
            thumbs=len(reviewer_likes) + len(writer_likes),
            thumb_list=like_list,
            comments=comment_count,
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
    return render(request, "v2/work.html", event_info)


def center(request):
    return render(request, "v2/center.html")


def login_v2(request):
    return render(request, "v2/login.html")


def login(request):
    return render(request, "login.html")


def info(request):
    return render(request, "info.html")
