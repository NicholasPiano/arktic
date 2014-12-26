#woot.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url

#local
from apps.distribution.views import ProjectView, JobView
from apps.pages.views import LoginView, StartView
from apps.transcription.views import TranscriptionView

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
  #distribution
  url(r'^projects/$', ProjectView.as_view()),
  url(r'^jobs/$', JobView.as_view()),

  #pages
  url(r'^login/$', LoginView.as_view()),
  url(r'^logout/$', 'django.contrib.auth.views.logout'),
  url(r'^start/$', StartView.as_view()),

  #transcription
  url(r'^transcription/(?P<job_id_token>[a-z0-9]{8})$', TranscriptionView.as_view()),
)
