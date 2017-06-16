from django.conf.urls import url, static
from QingningWork.settings import WORK_URL
from Work import views, front_views

urlpatterns = [
    # url(r'^detail/$', views.get_work_detail, name="get-work-detail"),
    # url(r'^comment/$', views.get_work_comments, name="get-work-comment"),
    url(r'^upload$', views.upload_work, name="upload-work"),
    # url(r'^delete/$', views.delete, name="delete-work-by-its-owner"),
    # url(r'^modify/$', views.modify, name="modify-work-by-its-owner"),
    url(r'^comment$', views.comment, name='comment-work'),
    url(r'^like$', views.like, name='like-work'),
    url(r'^comment/delete$', views.comment_delete, name='comment-delete')
] + [
    # url(r'^detail.view/(?P<wid>\d+)/', front_views.detail, name="front-page-work-detail"),
    # url(r'^upload.act/', front_views.upload, name="front-page-upload-work"),
]

urlpatterns += static.static('upload_files/', document_root=WORK_URL)
