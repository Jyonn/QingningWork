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

    reviewers = [
        Reviewer.create(
            username="re",
            pwd_login=True,
        ).set_password("re").save(),
    ]

    writers = [
        Writer.create(
            username="w",
            pwd_login=True,
        ).set_password("w").save(),
    ]

if __name__ == "__main__":
    main()
