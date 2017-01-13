from django.conf.urls import url
from Reviewer import views

urlpatterns = [
    url(r'^work/upload/', views.upload_work, name="upload-work-via-reviewer"),
]
