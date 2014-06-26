#transcription.models

#django
from django.db import models
from django.core.files import File
from django.db.models.fields.files import FileField

#local
from apps.transcription.fields import ContentTypeRestrictedFileField
from django.core.exceptions import ObjectDoesNotExist
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

spanish = 'es'
english = 'en'
language_choices = (
    (spanish, 'Spanish'),
    (english, 'English'),
)

#classes
class Archive(models.Model):
    #connections
    project = models.ForeignKey(Project, related_name='archives')
    #sub: relfiles, transcriptions

    #properties
    file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.project) + ' > ' + str(self.file) + ' > ' + str(self.date_created)

    #override methods
    def save(self, *args, **kwargs):
        if self.pk is None:
            super(Archive, self).save(*args, **kwargs)
            self.extract() #necessary here becasue this is done through the admin. When I write an upload view, this will not be necessary.
        else:
            super(Archive, self).save(*args, **kwargs) #first time

    #custom methods
    def extract(self):
        #open zip file and distribute into relfiles, transcriptions and autocomplete words
        zip_file_list = []

        zip_file = zp.ZipFile(self.file.file)
        for file_name in zip_file.namelist():
            zip_file_list.append(file_name)

        outer_zip_path, zip_ext = os.path.splitext(zip_file.filename)
        inner_zip_path = os.path.join(ARCHIVE_ROOT, outer_zip_path)
        zip_file.extractall(path=inner_zip_path)

        #sort into relfile an audio files
        for file_name in zip_file_list:
            if re.search(r'\w+\/$', file_name) is None and re.search(r'Unsorted', file_name) is None and re.search(r'.csv', file_name) is not None:
                with open(os.path.join(inner_zip_path, file_name)) as open_relfile:
                    file_subpath, relfile_file_name = os.path.split(file_name)
                    relfile = self.relfiles.create(client=self.project.client, project=self.project, name=relfile_file_name, file=File(open_relfile))
                    relfile.extract(inner_zip_path, zip_file_list)
                    relfile.save()

        sh.rmtree(os.path.join(inner_zip_path, outer_zip_path))

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
    language = models.CharField(max_length=3, choices=language_choices, default=english)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    #custom methods
    def update(self):
        if self.transcriptions.filter(is_active=True).count()==0:
            if self.is_active:
                self.is_active = False

    def extract(self, inner_zip_path, zip_file_list):
        #make dictionary of files
        file_dictionary = {}
        for file_name in zip_file_list:
            file_dictionary.update({os.path.basename(file_name):os.path.join(inner_zip_path, file_name)})
        #open file
        lines = self.file.file.readlines()
        for line_number, line in enumerate(lines):
            tokens = line.split('|') #this can be part of a relfile parser object with delimeter '|'
            transcription_audio_file_name = os.path.basename(tokens[0])
            grammar = os.path.splitext(os.path.basename(tokens[1]))[0]
            confidence = tokens[2]
            utterance = tokens[3]
            value = tokens[4]
            confidence_value = tokens[5].rstrip() #chomp newline
            if confidence_value is not '':
                confidence_value = float(float(confidence_value)/1000.0) #show as decimal
            else:
                confidence_value = 0.0

            #open file and create transcription
            with open(file_dictionary[transcription_audio_file_name]) as transcription_audio_file:
                self.transcriptions.create(client=self.client,
                                           project=self.project,
                                           archive=self.archive,
                                           audio_file=File(transcription_audio_file),
                                           line_number=line_number,
                                           grammar=grammar,
                                           confidence=confidence,
                                           utterance=utterance,
                                           value=value,
                                           confidence_value=confidence_value)

        self.client.create_autocomplete_words() #run once for every relfile.


class CompletedRelFile(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='completed_relfiles')
    project = models.ForeignKey(Project, related_name='completed_relfiles')
    archive = models.ForeignKey(Archive, related_name='completed_relfiles')
    relfile = models.ForeignKey(RelFile, related_name='completed_relfiles')
    #sub: transcriptions (null)

    #properties
    file = models.FileField(upload_to='completed_relfiles', max_length=255)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name + '_completed'

    #custom methods

class Transcription(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='transcriptions')
    project = models.ForeignKey(Project, related_name='transcriptions')
    archive = models.ForeignKey(Archive, related_name='transcriptions')
    job = models.ForeignKey(Job, null=True, related_name='transcriptions')
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
        return str(str(self.project) + ' > ').encode('utf-8') + self.utterance

    #custom methods
    def latest_revision_words(self, user):
        #delete current words
        for word in self.words.all():
            word.delete()
        #add new one
        try:
            latest_revision = self.revisions.latest()
            for word in latest_revision.words.all():
                self.words.create(content=word.content)
            #latest revision user
            self.latest_revision_done_by_current_user = user.pk == latest_revision.user.pk
        except ObjectDoesNotExist:
            pass

    def update(self):
        if self.revisions.all().count() > 0: #this should be adjusted in settings.
            if self.is_active:
                self.is_active = False

class TranscriptionWord(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content

class Revision(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='revisions')
    user = models.ForeignKey(User, related_name='revisions')
    #sub: revision words

    #properties
    utterance = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'blank' + ' to "' + str(self.utterance) +  '" by ' + str(self.user) if self.transcription.utterance=='' else str(self.transcription) + ' to "' + str(self.utterance) +  '" by ' + str(self.user)

    class Meta:
        get_latest_by = 'date_created'


class RevisionWord(models.Model):
    #connections
    revision = models.ForeignKey(Revision, related_name='words')

    #properties
    content = models.CharField(max_length=255)

    def __unicode__(self):
        return self.content
