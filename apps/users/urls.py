#users.urls

#django
from django.conf.urls import patterns, include, url

#local
from apps.users.views import StartView#, ProfileView
from apps.transcription.views import MainJobView

urlpatterns = (
    #start page
    url(r'^$', StartView.as_view()),
    url(r'^new/$', MainJobView.as_view()),
)
