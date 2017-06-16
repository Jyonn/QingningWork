"""QingningWork URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include, static
from django.contrib import admin
from AbstractUser import front_views

from QingningWork.settings import STATIC_FILE

urlpatterns = [
    url(r'^$', front_views.user),
    url(r'^v2/login$', front_views.login_v2, name='user-login-page'),
    url(r'^v2/center$', front_views.center, name='center-page'),
    url(r'^v2/center/review$', front_views.require_review, name='review-center-page'),
    url(r'^v2/center/follow$', front_views.follow_events, name='writer-center-page'),
    url(r'^v2/event/(?P<owner_id>\d+)/(?P<work_id>\d+)/(?P<event_id>\d+)$', front_views.event_page),
    url(r'^v2/thumbs/(?P<owner_id>\d+)/(?P<work_id>\d+)/(?P<event_id>\d+)$', front_views.thumb_page),
    url(r'^v2/comments/(?P<owner_id>\d+)/(?P<work_id>\d+)/(?P<event_id>\d+)$', front_views.comment_page),
    url(r'^v2/user/(?P<user_id>\d+)/(?P<role_id>\d+)', front_views.user_home),
    url(r'^v2/work/upload$', front_views.upload_work, name='upload-work-page'),
    url(r'^v2/work/style/(?P<work_id>\d+)/(?P<style_id>\d+)$', front_views.work_style, name='work-style-page'),

    url(r'^legacy/', include("Work.legacy_urls")),

    # url(r'^admin/', admin.site.urls),
    url(r'^user/', include("AbstractUser.urls")),
    # url(r'^reviewer/', include("Reviewer.urls")),
    url(r'^work/', include("Work.urls")),
    # url(r'^writer/', include("Writer.urls")),
    url(r'^base/', include("BaseFunc.urls")),
]

urlpatterns += static.static('/', document_root=STATIC_FILE)
