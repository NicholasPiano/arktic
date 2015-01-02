#apps.transcription.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url

#local
from apps.transcription.views import start_redirect, TranscriptionView, create_new_job, action_register, update_revision, add_word

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
  url(r'^$', start_redirect),
  url(r'^(?P<job_id_token>[A-Z0-9]{8})$', TranscriptionView.as_view()),
  url(r'^new/$', create_new_job),
  url(r'^action/$', action_register),
  url(r'^revision/$', update_revision),
  url(r'^add/$', add_word),
)
