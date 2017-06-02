from django.conf.urls import url
from . import legacy_views

urlpatterns = [
    url(r'^work-file-to-sql$', legacy_views.work_file_to_sql),
]