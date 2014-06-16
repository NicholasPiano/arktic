#transcription.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url

#local
from apps.transcription.views import MainTranscriptionView

#patterns
urlpatterns = patterns('',
    url(r'^$', 'apps.transcription.views.start_redirect', name='start_redirect'),
    url(r'^(?P<job_id>[0-9]+)/$', MainTranscriptionView.as_view()),
)
