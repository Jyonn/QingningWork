from django.conf.urls import url, static
from QingningWork.settings import WORK_URL
from Work import views, front_views

urlpatterns = [
    # url(r'^detail/$', views.get_work_detail, name="get-work-detail"),
    # url(r'^comment/$', views.get_work_comments, name="get-work-comment"),
    url(r'^upload$', views.upload),
    url(r'^delete$', views.delete),
    url(r'^modify$', views.modify),
    url(r'^comment$', views.comment),
    url(r'^like$', views.like),
    url(r'^comment/delete$', views.comment_delete),
    url(r'^set/privilege$', views.set_privilege)
] + [
    # url(r'^detail.view/(?P<wid>\d+)/', front_views.detail, name="front-page-work-detail"),
    # url(r'^upload.act/', front_views.upload, name="front-page-upload-work"),
]

urlpatterns += static.static('upload_files/', document_root=WORK_URL)
