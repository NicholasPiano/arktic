#django
from django.contrib import admin

#local
from distribution.models import Distributor, Job

admin.site.register(Distributor)
admin.site.register(Job)
