from AbstractUser.models import AbstractUser
from BaseFunc.base import response
from Comment.models import Comment
from QingningWork.settings import WORK_URL
from Reviewer.models import Reviewer
from Work.models import Work
from Timeline.models import Timeline

import base64

from Writer.models import Writer


def work_file_to_sql(request):
    works = Work.objects.all()
    for work in works:
        file_path = WORK_URL + work.work_store
        with open(file_path, "rb+") as f:
            content = f.read().decode()
            f.close()
        content = base64.decodebytes(bytes(content, encoding="utf8"))
        content = content.decode()
        work.content = content
        work.save()
    return response()


def work_calculate_newest(request):
    works = Work.objects.all()
    for work in works:
        w = work
        while True:
            try:
                w = Work.objects.get(last_version_work=w)
            except:
                break
        work.newest_version_work = w
        work.is_updated = work.newest_version_work != work
        work.save()

    return response()


def user_avatar_to_cdn(request):
    users = AbstractUser.objects.all()
    from random import randint
    for user in users:
        avatar_int = randint(1, 10)
        avatar_img = "0" if avatar_int < 10 else ""
        avatar_img += str(avatar_int)
        avatar_img = "img/avatar/default-" + avatar_img + ".jpg"
        user.avatar = avatar_img
        user.save()
    return response()


def create_qn_writer(request):
    w = Writer.create(
        username='青柠',
        pwd_login=True,
        introduce='以梦为马，不负韶华。',
    )
    w.set_password('QingNing2017').save()
    return response()


def update_work_create_to_timeline(request):
    default_writer = Writer.objects.get(username='青柠')
    works = Work.objects.all()
    for work in works:
        tl_type = Timeline.TYPE_CREATE_WORK if work.last_version_work is None else Timeline.TYPE_MODIFY_WORK
        writer = default_writer if work.re_writer is None else work.re_writer
        try:
            tl = Timeline.objects.get(related_work=work)
            tl.create_time = work.create_time
            tl.save()
            print(tl.create_time, work.create_time)
        except:
            Timeline.create(writer, work, tl_type, create_time=work.create_time)
    return response()


def comment_decode_base64(request):
    comments = Comment.objects.all()
    for comment in comments:
        comment.content = base64.decodebytes(bytes(comment.content_base64, encoding="utf8")).decode()
        comment.save()
    return response()


def update_abstract_user_type(request):
    writers = Writer.objects.all()
    for writer in writers:
        writer.user_id = writer.wid
        writer.user_type = AbstractUser.TYPE_WRITER
        writer.save()

    reviewers = Reviewer.objects.all()
    for reviewer in reviewers:
        reviewer.user_id = reviewer.rid
        reviewer.user_type = AbstractUser.TYPE_REVIEWER
        reviewer.save()

    return response()