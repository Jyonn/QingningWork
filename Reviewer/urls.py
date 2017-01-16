from django.conf.urls import url

from Reviewer import views, front_views

urlpatterns = [
    url(r'^work/upload/', views.upload_work, name="upload-work-via-reviewer"),
    url(r'^work/not-reviewed/', views.get_not_reviewed_list, name="get-not-reviewed-work-list"),
    url(r'^work/review/', views.review_work, name="review-work"),
    url(r'^info/', views.info, name="reviewer-information"),
] + [
    url(r'^center.view/', front_views.center, name="front-page-reviewer-center"),
]
