#django
from django.conf.urls import patterns, include, url

#local
from apps.transcription.views import MainJobView

urlpatterns = patterns('',
    url(r'^$', MainJobView.as_view()),
)
