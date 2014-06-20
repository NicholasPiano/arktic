#transcription.models

#django
from django.db import models
from django.core.files import File
from django.db.models.fields.files import FileField

#local
from apps.transcription.fields import ContentTypeRestrictedFileField
from settings.common import MEDIA_ROOT
from apps.distribution.models import Client, Project, Job
from apps.users.models import User

#util
import wave as wv
import numpy as np
import os
import re
import subprocess as sp
import zipfile as zp
import shutil as sh
import collections as cl
import string as st

#vars
ARCHIVE_ROOT = os.path.join(MEDIA_ROOT, 'archive')
COMPLETED_RELFILES_ROOT = os.path.join(MEDIA_ROOT, 'completed_relfiles')

#classes
class Archive(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='archives')
    project = models.ForeignKey(Project, related_name='archives')
    #sub: relfiles, transcriptions

    #properties
    file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Archive, self).save(*args, **kwargs)
        else:
            super(Archive, self).save(*args, **kwargs) #first time

    #custom methods

class RelFile(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='relfiles')
    project = models.ForeignKey(Project, related_name='relfiles')
    archive = models.ForeignKey(Archive, related_name='relfiles')
    #sub: transcriptions, autocomplete words

    #properties
    is_active = models.BooleanField(default=True)
    file = models.FileField(upload_to='relfiles', max_length=255)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(RelFile, self).save(*args, **kwargs)
        else:
            super(RelFile, self).save(*args, **kwargs) #first time

    #custom methods

class CompletedRelFile(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='completed_relfiles')
    project = models.ForeignKey(Project, related_name='completed_relfiles')
    archive = models.ForeignKey(Archive, related_name='completed_relfiles')
    relfile = models.OneToOneField(RelFile, related_name='completed_relfile')
    #sub: transcriptions (null)

    #properties
    file = models.FileField(upload_to='completed_relfiles', max_length=255)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time

    #custom methods

class Transcription(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='transcriptions')
    project = models.ForeignKey(Project, related_name='transcriptions')
    archive = models.ForeignKey(Archive, related_name='transcriptions')
    relfile = models.ForeignKey(RelFile, related_name='transcriptions')
    #sub: transcription words, revisions

    #properties
    audio_file = FileField(upload_to='audio', max_length=255) #use audiofield when done
    line_number = models.IntegerField()
    time = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
    grammar = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255)
    utterance = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
    requests = models.IntegerField(default=0) #number of times the transcription has been requested.
    add_date = models.DateTimeField(auto_now_add=True)
    date_last_requested = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    latest_revision_done_by_current_user = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time

    #custom methods
    def latest_revision_words(self):
        pass #get list of words from the latest revision

class TranscriptionWord(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time

class Revision(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='revisions')
    #sub: revision words

    #properties
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    class Meta:
        get_latest_by = 'date_created'

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time


class RevisionWord(models.Model):
    #connections
    revision = models.ForeignKey(Revision, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is not None:
            super(Client, self).save(*args, **kwargs)
        else:
            super(Client, self).save(*args, **kwargs) #first time
