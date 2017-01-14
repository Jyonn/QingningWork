from django.conf.urls import url, static
from QingningWork.settings import WORK_URL
from Work import views

urlpatterns = [
    url(r'^detail/', views.get_work_detail, name="get-work-detail"),
]

urlpatterns += static.static('upload_files/', document_root=WORK_URL)
