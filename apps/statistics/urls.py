#statistics.views

#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
from statistics.views import IndexView, ArchiveView, DistributionView, TranscriptionView, UsersView

urlpatterns = (
    #land
    url(r'^$', IndexView.as_view()),
    #archive
    url(r'^archive/', ArchiveView.as_view()),
    #distribution
    url(r'^distribution/', DistributionView.as_view()),
    #transcription
    url(r'^transcription/', TranscriptionView.as_view()),
    #users
    url(r'^users/', UsersView.as_view()),
)
