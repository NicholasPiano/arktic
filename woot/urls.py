#base.urls

#django
from django.contrib import admin
from django.conf.urls import patterns, include, url

#local

#third party

# See: https://docs.djangoproject.com/en/dev/ref/contrib/admin/#hooking-adminsite-instances-into-your-urlconf
admin.autodiscover()

# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',

)
