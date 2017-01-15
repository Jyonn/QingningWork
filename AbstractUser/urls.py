from django.conf.urls import url
from AbstractUser import views, front_views


urlpatterns = [
    url(r'^login/', views.login, name="user-login"),
    url(r'^logout/', views.logout, name="user-logout"),
    url(r'^username/change/', views.change_username, name="change-username"),
    url(r'^password/change/', views.change_password, name="change-password"),
    url(r'^password/unset/', views.unset_password, name="unset-password"),
] + [
    url(r'^login.act', front_views.index, name="front-page-login"),
]
