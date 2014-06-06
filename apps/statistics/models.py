#statistics.models

#django
from django.db import models

#local
from apps.distribution.models import Distributor, Job

# Create your models here.
class Statistics(models.Model):
    #connections
    distributor = models.OneToOneField(Distributor)

    #properties
