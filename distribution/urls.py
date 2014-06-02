#distribution.urls

#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
from distribution.views import IndexView, JobView

urlpatterns = (
    #land
    url(r'^$', IndexView.as_view()),
    #job
    url(r'^job/(?P<pk>\d+)/$', JobView.as_view()),
)
