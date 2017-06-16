from django.conf.urls import url
from . import legacy_views

urlpatterns = [
    url(r'^work-file-to-sql$', legacy_views.work_file_to_sql),
    url(r'^work-calculate-newest$', legacy_views.work_calculate_newest),
    url(r'^user-avatar-to-cdn$', legacy_views.user_avatar_to_cdn),
    url(r'^create-qn-writer$', legacy_views.create_qn_writer),
    url(r'^update-work-create-to-timeline$', legacy_views.update_work_create_to_timeline),
    url(r'^comment-decode-base64$', legacy_views.comment_decode_base64),
    url(r'^update-abstract-user-type$', legacy_views.update_abstract_user_type),

    url(r'^create-timeline', legacy_views.create_timeline),
]
