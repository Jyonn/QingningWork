from BaseFunc.base import response
from QingningWork.settings import WORK_URL
from Work.models import Work


def work_file_to_sql(request):
    works = Work.objects.all()
    for work in works:
        file_path = WORK_URL + work.work_store
        with open(file_path, "rb+") as f:
            content = f.read().decode()
            f.close()
        print(content)
        break
    return response()
