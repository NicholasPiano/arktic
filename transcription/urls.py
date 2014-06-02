#django
from django.conf.urls import patterns, include, url

#local
from transcription.views import index

urlpatterns = patterns('',
    url(r'', index, name='index'),
)
