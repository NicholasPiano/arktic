#distribution.models

#django
from django.db import models

#local
from users.models import Employee as User

#util

class Distributor(models.Model):
    #properties
    name = models.CharField(max_length=100)
    #init

    #instance methods
    def __unicode__(self):
        return self.name


    #delete
    def delete(self, *args, **kwargs):
        #archives
        for archive in self.archives.all():
            archive.delete() #call custom delete method

        super(Distributor, self).delete(*args, **kwargs)

class Job(models.Model):
    #properties
    distributor = models.ForeignKey(Distributor, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')
    date_created = models.DateTimeField(auto_now_add=True)
