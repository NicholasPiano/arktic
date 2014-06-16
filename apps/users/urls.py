#users.urls

#django
from django.conf.urls import patterns, include, url

#local
from apps.users.views import StartView

urlpatterns = (
    #start page
    url(r'^$', StartView.as_view()),
    url(r'^new/$', 'apps.users.views.create_new_job', name='new-job'),
)
