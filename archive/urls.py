#archive.urls

#django
from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

#local
from archive.views import IndexView, UploadView

urlpatterns = (
    #land
    url(r'^$', IndexView.as_view()),
    #upload
    url(r'^upload/', UploadView.as_view()),
)
