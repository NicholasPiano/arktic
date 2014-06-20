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

#class vars
ARCHIVE_ROOT = os.path.join(MEDIA_ROOT, 'archive')
COMPLETED_ROOT = os.path.join(MEDIA_ROOT, 'completed')

#vars
WAV_TYPE = 'wav'
transcription_types = [
    'yes-no',
]

#class methods
def zipdir(path, zip):
    for root, dirs, files in os.walk(path):
        for file in files:
            zip.write(os.path.join(root, file))

#classes
class Archive(models.Model):
    #properties
    client = models.ForeignKey(Client, related_name='archives')
    file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])
    date_created = models.DateTimeField(auto_now_add=True)
    #sub: relfiles

    #save
    def save(self, *args, **kwargs):
        if self.pk is None: #if the archive is being uploaded for the first time
            super(Archive, self).save(*args, **kwargs)
            self.extract(*args, **kwargs)
        else:
            super(Archive, self).save(*args, **kwargs)

    def extract(self, *args, **kwargs):
        #1. extract zip
        file_list = []

        zip_file = zp.ZipFile(self.file.file)
        for name in zip_file.namelist():
            file_list.append(name)

        extract_tree, ext = os.path.splitext(zip_file.filename)
        extract_path = os.path.join(ARCHIVE_ROOT, extract_tree)
        zip_file.extractall(path=extract_path)

        #2. sort into relfile and audio files - first make relfile from each object, then validate.
        relfile_index = 0
        for file in file_list:
            if re.search(r'\w+\/$', file) is None and re.search(r'Unsorted', file) is None: #matches trailing slash to weed out directories
                if re.search(r'.csv', file) is not None: #relfile
                    print('relfile_index: ' + str(relfile_index))
                    relfile_index += 1
                    open_file = File(open(os.path.join(extract_path, file)))
                    (file_subpath, filename) = os.path.split(file) #path splitter os.path.split
                    self.relfiles.create(file=open_file, name=filename)

        #3. link relfiles and transcriptions
        big_transcription_dictionary = {}
        for relfile in self.relfiles.all():
            big_transcription_dictionary.update(relfile.transcription_dictionary)

        print('transcription_dictionary_size: ' + str(len(big_transcription_dictionary)))

        audio_file_index = 0
        succesful = 0
        keyerror = 0
        for audio_file in file_list:
            if re.search(r'\w+\/$', audio_file) is None: #matches trailing slash to weed out directories
                if re.search(r'.wav', audio_file) is not None: #audio
                    audio_file_index += 1
                    try:
                        succesful += 1
                        file_name = os.path.basename(audio_file)
                        kwargs = big_transcription_dictionary[file_name]
                        relfile_id = kwargs.pop('relfile_id')
                        relfile = self.relfiles.get(pk=relfile_id)

                        with open(os.path.join(extract_path, audio_file)) as f:
                            open_file = File(f)
                            kwargs['audio_file'] = open_file
                            kwargs['relfile'] = relfile
#                             print(kwargs)
                            t = self.client.transcriptions.create(**kwargs) #create while file is open
                            t.save()
                            #file is then automatically closed by 'with'.

                    except KeyError:
                        print('keyerror: ' + str(os.path.basename(audio_file)))
                        print(kwargs)
                        print('audio_file_index: ' + str([audio_file_index, succesful, keyerror]))
                        keyerror += 1

        #4. remove extract tree after use
        sh.rmtree(os.path.join(extract_path, extract_tree))

    def compress(self): #package for download when all constituent transcriptions are complete
        #filename
        new_zip_filename = os.path.splitext(os.path.basename(self.file.name))[0] #u'archive/file.zip' -> 'file'
        new_zip_filename += '.out.zip' #'file' -> 'file.out.zip'
        print(new_zip_filename)
        #remove any previous compression
        if os.path.isfile(os.path.join(COMPLETED_ROOT, new_zip_filename)): #if file already exists
            os.remove(os.path.join(COMPLETED_ROOT, new_zip_filename))
        #open zipfile
        #1. extract zip
        file_list = []

        zip_file = zp.ZipFile(self.file.file)
        for name in zip_file.namelist():
            file_list.append(name)

        extract_tree, ext = os.path.splitext(os.path.basename(zip_file.filename))
        extract_path = os.path.join(COMPLETED_ROOT, extract_tree)
        zip_file.extractall(path=extract_path)

        #open each relfile
        #-get contents
        #-replace lines with those from transcription revisions
        #-write to new files with '.out.csv' appended
        #-remove original relfile
        for file in file_list:
            if re.search(r'\w+\/$', file) is None: #matches trailing slash to weed out directories
                if re.search(r'.csv', file) is not None: #relfile
                    file_subpath, filename = os.path.split(file)
                    file_root = os.path.splitext(filename)[0]
                    new_lines = []
                    with open(os.path.join(extract_path, file), 'r') as open_relfile:
                        lines = open_relfile.readlines()
                        for line_number, line in enumerate(lines):
                            tokens = line.split('|')
                            grammar = os.path.splitext(os.path.basename(tokens[1]))[0] #grammar different from relfile name
                            transcription = self.client.transcriptions.get(line_number=line_number, grammar=grammar)
                            print([grammar, line_number, transcription.utterance, tokens[3]])
                            revision = transcription.revisions.latest() #must exist, otherwise would not be in this method
                            tokens[3] = revision.utterance #utterance
                            new_line = '|'.join(tokens)
                            new_lines.append(new_line)
                    new_filename = file_root + '.out.csv'
                    with open(os.path.join(extract_path, os.path.join(file_subpath, new_filename))) as new_relfile:
                        for line in new_lines:
                            new_relfile.write(line + '\n')

        #recompress archive into archive.out.zip


    def check_transcriptions(self): #check if all transcriptions have a revision. If so, compress
        #each transcription in each relfile must have a revision object
        will_compress = True
        for relfile in self.relfiles.all():
            for transcription in relfile.transcriptions.all():
                if not transcription.revisions.all():
                    will_compress = False
                    break; #even if one transcription is incomplete
        if will_compress:
            self.compress()

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

class CompletedArchive(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='completed_archives')
    archive = models.OneToOneField(Archive, related_name='completed_archive')

    #properties
    file = ContentTypeRestrictedFileField(upload_to='completed', max_length=255, content_types=['application/zip'])
    date_created = models.DateTimeField(auto_now_add=True)

class RelFile(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='relfiles')
    project = models.ForeignKey(Project, related_name='relfiles')
    archive = models.ForeignKey(Archive, related_name='relfiles')

    #properties
    file = models.FileField(upload_to='relfile', max_length=255) #switch to audiofield when ready
    name = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)
    transcription_dictionary = {}

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(RelFile, self).save(*args, **kwargs)
        #parse into audio file name list and create transcription objects
        #1. read lines
        lines = self.file.file.readlines()
        #2. for each lines, get audio_file name, utterance, any other information
        for line_index in range(len(lines)):
            line = lines[line_index]
            line_split = line.split('|') #always a pipe, and always 5 columns
            file_name = os.path.basename(line_split[0])
            if line_index==22:
                print([self.pk, line_split[1], line_split[3]])
            self.transcription_dictionary[file_name] = {
                'relfile_id':self.pk,
                'line_number':line_index,
                'grammar':line_split[1],
                'confidence':line_split[2],
                'utterance':line_split[3],
                'value':line_split[4],
                'confidence_value':line_split[5],
            }

class Transcription(models.Model):
    #connections
    client = models.ForeignKey(Client, related_name='transcriptions')
    project = models.ForeignKey(Project, related_name='transcriptions')
    archive = models.ForeignKey(Archive, related_name='transcriptions')
    relfile = models.ForeignKey(RelFile, related_name='transcriptions')
    job = models.ForeignKey(Job, null=True, related_name='transcriptions')

    #properties
    type = models.CharField(max_length=100)
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

    def __init__(self, *args, **kwargs):
        if kwargs:
            #modify keywords
            #-grammar
            kwargs['grammar'] = os.path.splitext(os.path.basename(kwargs['grammar']))[0] #just get grammar name
            #-confidence_value
            confidence_value = kwargs['confidence_value'].rstrip() #chomp
            if confidence_value is not '':
                kwargs['confidence_value'] = float(float(confidence_value)/1000.0) #show as decimal
            else:
                kwargs['confidence_value'] = 0.0

        super(Transcription, self).__init__(*args, **kwargs)

    def __unicode__(self):
        return self.utterance

    #save - always called by 'create'
    def save(self, *args, **kwargs):
        if self.pk is None: #if the archive is being uploaded for the first time
            super(Transcription, self).save(*args, **kwargs)
            self.configure()
        else:
            super(Transcription, self).save(*args, **kwargs)

    def configure(self):
        self.time = len(self.utterance)/10.0 #number of characters divided by ten (completely arbitrary)

    def latest_revision_words(self):
        latest_revision_words = []
        try:
            latest_revision = self.revisions.latest()
            latest_revision_words = latest_revision.words.all()
            user = self.job.user
            self.latest_revision_done_by_current_user = latest_revision.user.pk == user.pk
        except Revision.DoesNotExist:
            self.latest_revision_done_by_current_user = False
        for word in self.words.all(): #remove current words
            word.delete()
        for word in latest_revision_words:
            self.words.create(char=word)

class TranscriptionWord(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='words')

    #properties
    char = models.CharField(max_length=100)

    def __unicode__(self):
        return self.char

class Revision(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='revisions')
    user = models.ForeignKey(User, related_name='revisions')

    #properties
    utterance = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        get_latest_by = 'date_created'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            for word in self.utterance.split():
                self.words.create(char=word)
            super(Revision, self).save(*args, **kwargs)
        else:
            super(Revision, self).save(*args, **kwargs)

    def __unicode__(self):
        return 'Revision of #' + str(self.transcription.pk) + ' by ' + str(self.user) + ': "' + self.utterance + '" on ' + str(self.date_created) #maybe also format date

class RevisionWord(models.Model):
    #connections
    revision = models.ForeignKey(Revision, related_name='words')

    #properties
    char = models.CharField(max_length=100)

    def __unicode__(self):
        return self.char
