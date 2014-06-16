#arktic.urls

#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
from apps.pages.views import IndexView, AboutView, SystemView, PricesView, SecurityView, LoginView

urlpatterns = patterns('',
    #home and client side
    url(r'^$', IndexView.as_view()),
    #-about
    url(r'^about/', AboutView.as_view()),
    #-system
    url(r'^system/', SystemView.as_view()),
    #-prices
    url(r'^prices/', PricesView.as_view()),
    #-security
    url(r'^security/', SecurityView.as_view()),

    #login
    url(r'^login/$', LoginView.as_view()),
    url(r'^logout/$', 'django.contrib.auth.views.logout',{'next_page': '/login/'}),

    #admin
    url(r'^admin/', include(admin.site.urls)),
    #-statistics interface
#     url(r'^statistics/', include('statistics.urls', namespace='statistics')),
    #-distribution
    url(r'^distribution/', include('apps.distribution.urls', namespace='distribution')),

    #employee
    #-landing page
    url(r'^start/', include('apps.users.urls', namespace='users')),
    #-main transcription interface
    url(r'^transcription/', include('apps.transcription.urls', namespace='transcription')),
)
