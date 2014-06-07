#users.models

#django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

#local
from apps.distribution.models import Client, Job

class User(models.Model):
    user = models.OneToOneField(User,
                                unique=True,
                                verbose_name=_('employee'))

    def __unicode__(self):
        return self.user.username

    def create_job_for_client(self, client_name):
        #make job
        job = self.jobs.create(client_id=client_name)
        job.get_transcription_set()
        job.save()
