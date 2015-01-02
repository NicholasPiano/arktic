#woot.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url
from settings.common import MEDIA_ROOT

#local
from apps.pages.views import LoginView, StartView, logout_view

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
  # Serving media
  url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True }),

  #pages
  url(r'^login/$', LoginView.as_view()),
  url(r'^logout/$', logout_view),
  url(r'^$', StartView.as_view()),
  url(r'^start/$', StartView.as_view()),

  #transcription
  url(r'^transcription/', include('apps.transcription.urls')),
  url(r'^new/', 'apps.transcription.views.create_new_job'),

  #admin
  url(r'^admin/', include(admin.site.urls)),
)

#1. make users
#2. make jobs
#3. make transcription url work
#4. make start url work
#5. latest revision words
#6.
