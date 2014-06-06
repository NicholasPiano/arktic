#django
from django.contrib import admin

#local
from apps.distribution.models import Distributor, Job

# Register your models here.
#job
admin.site.register(Job)

#distributor

admin.site.register(Distributor)
