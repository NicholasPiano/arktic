#statistics.models

#django
from django.db import models

#local
from archive.models import Archive, RelFile
from distribution.models import Distributor, Job

# Create your models here.
class Statistics(models.Model):
    #connections
    distribution = models.OneToOneField(Distributor)

    #properties
