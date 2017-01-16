from django.conf.urls import url, static
from AbstractUser import views, front_views
from QingningWork.settings import AVATAR_URL

urlpatterns = [
    url(r'^login/', views.login, name="user-login"),
    url(r'^status/', views.status, name="user-status"),
    url(r'^logout/', views.logout, name="user-logout"),
    url(r'^username/change/', views.change_username, name="change-username"),
    url(r'^password/change/', views.change_password, name="change-password"),
    url(r'^password/unset/', views.unset_password, name="unset-password"),
] + [
    url(r'^login.act/', front_views.login, name="front-page-login"),
]

urlpatterns += static.static('avatar/', document_root=AVATAR_URL)

