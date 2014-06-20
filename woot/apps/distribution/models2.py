#distribution.models

#django
from django.db import models
from django.db.models.fields.files import FileField
from django.core.files import File

#local
from apps.users.models import User
from settings.common import MEDIA_ROOT, NUMBER_OF_TRANSCRIPTIONS_PER_JOB

#util
import os

#vars

#classes

class Client(models.Model):
    #connections
    #sub: projects, jobs, archives, relfiles, transcriptions, autocomplete words

    #properties
    name = models.CharField(max_length=255)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time

    #custom methods

class Project(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='projects')
    #sub: jobs, archives, relfiles, transcriptions

    #properties
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Project, self).save(*args, **kwargs)
        else:
            super(Project, self).save(*args, **kwargs) #first time

    #custom methods

class CompletedProject(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='projects')
    #sub: completed relfiles

    #properties
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='completed', max_length=255)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(CompletedProject, self).save(*args, **kwargs)
        else:
            super(CompletedProject, self).save(*args, **kwargs) #first time

    #custom methods

class Job(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='jobs')
    project = models.ForeignKey(Project, related_name='jobs')
    user = models.ForeignKey(User, related_name='jobs')

    #properties
    is_active = models.BooleanField(default=True)
    active_transcriptions = models.IntegerField(default=NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
    total_transcription_time = models.DecimalField(max_digits=5, decimal_places=5, default=0.0)
    date_created = models.DateTimeField(auto_now_add=True)
    time_taken = models.DecimalField(max_digits=5, decimal_places=5, default=0.0)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Job, self).save(*args, **kwargs)
        else:
            super(Job, self).save(*args, **kwargs) #first time

    #custom methods

class Action(models.Model):
    #connections
    job = models.ForeignKey(Job, related_name='actions')
    user = models.ForeignKey(User, related_name='actions')

    #properties
    button_id = models.CharField(max_length=100)
    transcription_id = models.CharField(max_length=100)
    transcription_utterance = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Action, self).save(*args, **kwargs)
        else:
            super(Action, self).save(*args, **kwargs) #first time

    #custom methods

class AutocompleteWord(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(AutocompleteWord, self).save(*args, **kwargs)
        else:
            super(AutocompleteWord, self).save(*args, **kwargs) #first time

    #custom methods
