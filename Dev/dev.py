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
        Reviewer.create(username="924349668", pwd_login=False),
        Reviewer.create(username="1924846965", pwd_login=False),
        Reviewer.create(username="842176277", pwd_login=False),
        Reviewer.create(username="1143042604", pwd_login=False),
        Reviewer.create(username="1877936849", pwd_login=False),
        Reviewer.create(username="872407523", pwd_login=False),
        Reviewer.create(username="1974768911", pwd_login=False),
        Reviewer.create(username="1097452508", pwd_login=False),
        Reviewer.create(username="1176264560", pwd_login=False),
        Reviewer.create(username="jzdxq", pwd_login=False),
    ]

if __name__ == "__main__":
    main()
