#django
from django.conf.urls import patterns, include, url

#local
from transcription.views import index, next

urlpatterns = patterns('',
    url(r'^$', index, name='index'),
    url(r'^next/$', next, name='next')
)
