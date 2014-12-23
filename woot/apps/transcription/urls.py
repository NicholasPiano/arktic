#woot.apps.transcription.urls

#django

#local

#patterns
urlpatterns = patterns('',
  url(r'^$', 'apps.transcription.views.start_redirect', name='start_redirect'),
  url(r'^(?P<job_id>[0-9]+)/$', MainTranscriptionView.as_view()),
)
