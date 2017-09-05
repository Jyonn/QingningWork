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

    from Reviewer.models import Reviewer
    Reviewer.objects.get(username=679).set_password('lqj679ssn')


if __name__ == "__main__":
    main()
