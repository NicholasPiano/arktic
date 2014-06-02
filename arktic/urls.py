#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
from arktic.views import IndexView, AboutView, SystemView, PricesView, SecurityView, LoginView

urlpatterns = patterns('',
    #home and client side
    url(r'^$', IndexView.as_view()),
    #-about
    url(r'^$', AboutView.as_view()),
    #-system
    url(r'^$', SystemView.as_view()),
    #-prices
    url(r'^$', PricesView.as_view()),
    #-security
    url(r'^$', SecurityView.as_view()),

    #login
    url(r'^login/', LoginView.as_view()),

    #admin
    url(r'^admin/', include(admin.site.urls)),
    #-archive upload form
    url(r'^archive/', include('archive.urls', namespace='archive')),
    #-statistics interface
    url(r'^statistics/', include('statistics.urls', namespace='statistics')),
    #-distribution interface
    url(r'^distribution/', include('distribution.urls', namespace='distribution')),

    #employee
    #-landing page
    url(r'^start/', include(users.urls)),
    #-main transcription interface
    url(r'^transcription/', include('transcription.urls', namespace='transcription')),
)
