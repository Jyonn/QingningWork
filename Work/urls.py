from django.conf.urls import url, static
from QingningWork.settings import WORK_URL
from Work import views, front_views

urlpatterns = [
    url(r'^detail/', views.get_work_detail, name="get-work-detail"),
    url(r'^upload/', views.upload_work, name="upload-work-via-reviewer-or-writer"),
] + [
    url(r'^detail.view/(?P<wid>\d+)/', front_views.detail, name="front-page-work-detail"),
    url(r'^upload.act/', front_views.upload, name="front-page-upload-work"),
]

urlpatterns += static.static('upload_files/', document_root=WORK_URL)
