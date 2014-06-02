#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
import transcription

urlpatterns = patterns('',
    #home and client side
    # url(r'^$', 'arktic.views.home', name='home'),
    #-about
    #-system
    #-prices
    #-security

    #login
    # url(r'^login', 'arktic.views.login', name='login'),

    #admin
    url(r'^admin/', include(admin.site.urls)),
    #-archive upload form
    # url(r'^archive/', include(archive.urls)),
    #-statistics interface
    # url(r'^statistics/', include(statistics.urls)),

    #employee
    #-landing page
    # url(r'^start/', include(users.urls)),
    #-main transcription interface
    url(r'^transcription/', include('transcription.urls', namespace='transcription')),
)

#
