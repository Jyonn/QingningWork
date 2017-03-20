# coding=utf-8
def main():
    import sys
    import os

    os.environ['DB_INIT_SCRIPT'] = 'True'

    if os.path.dirname(__file__) != '':
        os.chdir(os.path.dirname(__file__) + os.sep + os.path.pardir)
    else:
        os.chdir(os.path.pardir)

    cwd = os.getcwd()
    sys.path.insert(0, cwd)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "QingningWork.settings")

    import django
    django.setup()

    from AbstractUser.models import AbstractUser
    from Comment.models import Comment
    from Reviewer.models import Reviewer
    from Writer.models import Writer
    from Work.models import Work
    # from Tag.models import Tag

    Comment.objects.all().delete()
    # Tag.objects.all().delete()
    Work.objects.all().delete()
    Writer.objects.all().delete()
    Reviewer.objects.all().delete()
    AbstractUser.objects.all().delete()

    reviewers = [
        Reviewer.create(username="re", pwd_login=True),
        Reviewer.create(username="re1", pwd_login=True),
        Reviewer.create(username="re2", pwd_login=True),
        Reviewer.create(username="re3", pwd_login=True),
        Reviewer.create(username="re4", pwd_login=True),
    ]
    reviewers[0].set_password("re").save()
    reviewers[1].set_password("re1").save()
    reviewers[2].set_password("re2").save()
    reviewers[3].set_password("re3").save()
    reviewers[4].set_password("re4").save()

    writers = [
        Writer.create(username="w", pwd_login=True),
        Writer.create(username="w1", pwd_login=True),
        Writer.create(username="w2", pwd_login=True),
        Writer.create(username="w3", pwd_login=True),
        Writer.create(username="w4", pwd_login=True),
    ]
    writers[0].set_password("w").save()
    writers[1].set_password("w1").save()
    writers[2].set_password("w2").save()
    writers[3].set_password("w3").save()
    writers[4].set_password("w4").save()

    works = [
        Work.create(
            re_reviewer=reviewers[0],
            writer_name="小寒",
            work_name="修炼爱情",
            work_store="0.txt",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2000-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[0],
            writer_name="工刀",
            work_name="那些你很冒险的梦",
            work_store="1.txt",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2001-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[0],
            writer_name="可大",
            work_name="爱笑的眼睛",
            work_store="2.doc",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2002-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[1],
            writer_name="茅莓",
            work_name="学不会",
            work_store="3.txt",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2003-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[1],
            writer_name="养乐多",
            work_name="可惜没如果",
            work_store="4.txt",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2004-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[1],
            writer_name="夏紫薇",
            work_name="期待爱",
            work_store="5.doc",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2005-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[1],
            writer_name="林俊杰",
            work_name="莎士比亚的天分",
            work_store="6.doc",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2006-01-01 20:00:00",
        ),
        Work.create(
            re_reviewer=reviewers[2],
            writer_name="海绵宝宝",
            work_name="黑键",
            work_store="7.doc",
            work_type=Work.WORK_TYPE_FILE,
            status=Work.STATUS_UNDER_REVIEW,
            create_time="2007-01-01 20:00:00",
        ),
    ]

    reviewers[0].total_upload = 3
    reviewers[1].total_upload = 4
    reviewers[2].total_upload = 1
    reviewers[0].save()
    reviewers[1].save()
    reviewers[2].save()

if __name__ == "__main__":
    main()
