#transcription.models

#django
from django.core.files import File
from django.db import models
from django.db.models.fields.files import FileField

#local
# from transcription.fields import AudioField
from apps.transcription.base_model import Model
from apps.transcription.fields import ContentTypeRestrictedFileField
from arktic.settings import MEDIA_ROOT
from apps.users.models import User
from apps.distribution.models import Client, Job

#util
import wave as wv
import numpy as np
import os
import re
import subprocess as sp
import zipfile as zp
import shutil as sh

#class vars
ARCHIVE_ROOT = os.path.join(MEDIA_ROOT, 'archive')

#########################################################################################################################
######################
############################################     Transcription unit
#vars
WAV_TYPE = 'wav'
transcription_types = [
    'yes-no',
]

class Transcription(Model):
    #connections
    client = models.ForeignKey(Client, related_name='transcriptions')
    job = models.ForeignKey(Job, null=True, related_name='transcriptions')
    users = models.ManyToManyField(User)

    #properties
    type = models.CharField(max_length=100)
    audio_file = FileField(upload_to='audio', max_length=255) #use audiofield when done
    time = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
    grammar = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255)
    utterance = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
    requests = models.IntegerField(default=0) #number of times the transcription has been requested.
    add_date = models.DateTimeField(auto_now_add=True)
    date_last_requested = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            #modify keywords
            #-grammar
            kwargs['grammar'] = os.path.splitext(os.path.basename(kwargs['grammar']))[0] #just get grammar name
            #-confidence_value
            confidence_value = kwargs['confidence_value'].rstrip() #chomp newline
            if confidence_value is not '':
                kwargs['confidence_value'] = float(float(confidence_value)/1000.0) #show as decimal
            else:
                kwargs['confidence_value'] = 0.0
            #time
            self.time = len(kwargs['utterance'])/10.0 #number of characters divided by ten (completely arbitrary)

        super(Transcription, self).__init__(*args, **kwargs)
#         self.audio_file.file.close()

    def __unicode__(self):
        return self.utterance

    #save - always called by 'create'
    def save(self, *args, **kwargs):
        super(Transcription, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.audio_file.delete(save=False)
        super(Transcription, self).delete(*args, **kwargs)

class Revision(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='revisions')

    #properties

class Action(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='actions')

    #properties

###################### Transcription unit ^^^
#########################################################################################################################

#########################################################################################################################
######################
############################################     Archive
#vars

class Archive(models.Model):
    #properties
    client = models.ForeignKey(Client, related_name='archives')
    file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])

    #save
    def save(self, *args, **kwargs):
        if self.pk is None: #if the archive is being uploaded for the first time
            super(Archive, self).save(*args, **kwargs)
            self.extract(*args, **kwargs)
        else:
            super(Archive, self).save(*args, **kwargs)

    def extract(self, *args, **kwargs):
        #1. extract zip
        self.file_list = []

        self.zip_file = zp.ZipFile(self.file.file)
        for name in self.zip_file.namelist():
            self.file_list.append(name)

        self.extract_tree, self.ext = os.path.splitext(self.zip_file.filename)
        self.extract_path = os.path.join(ARCHIVE_ROOT, self.extract_tree)
        self.zip_file.extractall(path=self.extract_path)

        #2. sort into relfile and audio files - first make relfile from each object, then validate.
        for file in self.file_list:
            if re.search(r'\w+\/$', file) is None: #matches trailing slash to weed out directories
                if re.search(r'.csv', file) is not None: #relfile
                    open_file = File(open(os.path.join(self.extract_path, file)))
                    (file_subpath, filename) = os.path.split(file) #path splitter os.path.split
                    self.relfiles.create(file=open_file, name=filename)

        #3. link relfiles and transcriptions
        big_transcription_dictionary = {}
        for relfile in self.relfiles.all():
            big_transcription_dictionary.update(relfile.transcription_dictionary)

        for audio_file in self.file_list:
            if re.search(r'\w+\/$', audio_file) is None: #matches trailing slash to weed out directories
                if re.search(r'.wav', audio_file) is not None: #relfile
                    try:
                        file_name = os.path.basename(audio_file)
                        kwargs = big_transcription_dictionary[file_name]

                        with open(os.path.join(self.extract_path, audio_file)) as f:
                            open_file = File(f)
                            kwargs['audio_file'] = open_file
                            self.client.transcriptions.create(**kwargs) #create while file is open
                            #file is then automatically closed by 'with'.

                    except KeyError:
                        pass

        #4. remove extract tree after use
        sh.rmtree(os.path.join(self.extract_path, self.extract_tree))

    #instance methods
    def __unicode__(self):
        return self.file.name

    def delete(self, *args, **kwargs):
        #delete actual zip files
        self.file.delete(save=False)

        #also delete files from relfiles/audio files, cos it wont happen in relfile.delete
        for relfile in self.relfiles.all():
            relfile.file.delete(save=False)

        super(Archive, self).delete(*args, **kwargs)


class RelFile(models.Model):
    #properties
    archive = models.ForeignKey(Archive, related_name='relfiles')
    file = models.FileField(upload_to='relfile', max_length=255) #switch to audiofield when ready
    name = models.CharField(max_length=100)
    transcription_dictionary = {}

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(RelFile, self).save(*args, **kwargs)
        #parse into audio file name list and create transcription objects
        #1. read lines
        lines = self.file.file.readlines()
        #2. for each lines, get audio_file name, utterance, any other information
        for line in lines:
            line_split = line.split('|') #always a pipe, and always 5 columns
            file_name = os.path.basename(line_split[0])
            self.transcription_dictionary[file_name] = {
                'grammar':line_split[1],
                'confidence':line_split[2],
                'utterance':line_split[3],
                'value':line_split[4],
                'confidence_value':line_split[5],
            }

    def delete(self, *args, **kwargs):
        self.file.delete(save=False)
        super(RelFile, self).delete(*args, **kwargs)

###################### Archive ^^^
#########################################################################################################################
