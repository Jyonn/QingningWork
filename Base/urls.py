from django.conf.urls import url
from Base import views

urlpatterns = [
    url(r'^captcha/img/$', views.get_image_captcha, name="get-image-captcha"),
]

