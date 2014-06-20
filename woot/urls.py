#base.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url

#local
from apps.pages.views import LoginView
from apps.users.views import StartView
from settings.common import MEDIA_ROOT

#third party
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    # Serving media
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True }),

    # Admin panel and documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Login
    url(r'^$', LoginView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/'}),

    # Users
    url(r'^start/$', StartView.as_view()),
    url(r'^new/$', 'apps.users.views.create_new_job', name='new'),

    # Transcription
    url(r'^transcription/', include('apps.transcription.urls', namespace='transcription')), #note: open ended for job number

    # Progress bar upload
    url(r'^progressbarupload/', include('progressbarupload.urls')),

    # Dajax
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
