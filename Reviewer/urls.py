from django.conf.urls import url

from Reviewer import views, front_views

urlpatterns = [
    # url(r'^work/not-reviewed/$', views.get_not_reviewed_list, name="get-not-reviewed-work-list"),
    url(r'^work/review/$', views.review_work, name="review-work"),
    url(r'^work/related/$', views.get_related_lists, name="get-related-works"),
    url(r'^work/bind-writer/$', views.bind_writer, name="bind-work-to-writer"),
    url(r'^info/$', views.info, name="reviewer-information"),
    url(r'^rank/$', views.rank, name="reviewer-rank"),
] + [
    url(r'^center.view/$', front_views.center, name="front-page-reviewer-center"),
    url(r'^rank.view/(?P<rank_type>\w+)/$', front_views.rank, name="rank-of-reviewers"),
]
