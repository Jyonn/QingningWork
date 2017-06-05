from django.conf.urls import url
from BaseFunc import views

urlpatterns = [
    url(r'^captcha/img$', views.get_image_captcha, name="get-image-captcha"),
]
