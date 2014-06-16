#users.models

#django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

#local

class User(models.Model):
    #connections
    user = models.OneToOneField(User, unique=True, verbose_name=_('user'))
    #sub: jobs
    #sub: revisions

    #properties
    #-auth

    #-performance
    average_time_per_transcription = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)

    def __unicode__(self):
        return self.user.username
