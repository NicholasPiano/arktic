#django
from django.conf.urls import patterns, include, url

#local
from apps.transcription.views import MainJobView

urlpatterns = patterns('',
    url(r'^(?P<job_id>[0-9]+)/$', MainJobView.as_view()),
)
