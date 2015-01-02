#apps.transcription.models

#django
from django.db import models
from django.core.files import File
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist

#local
from apps.distribution.models import Client, Project, Job
from apps.users.models import User
from libs.utils import generate_id_token, process_audio

#util
import os
from datetime import datetime as dt
import json

#vars

#classes
class Grammar(models.Model):
  ''' Stores all information about a single grammar: relfile, archive, transcriptions '''
  #types
  language_choices = (
    ('en','english'),
    ('es','spanish'),
  )

  #connections
  client = models.ForeignKey(Client, related_name='grammars')
  project = models.ForeignKey(Project, related_name='grammars')

  #properties
  is_active = models.BooleanField(default=False)
  id_token = models.CharField(max_length=8, null=True)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  date_completed = models.DateTimeField(auto_now_add=False, null=True)
  language = models.CharField(max_length=255, choices=language_choices, default='english')
  complete_rel_file = models.FileField(upload_to='completed')

  #methods
  def __str__(self):
    return '%s > %s > %d:%s > %s'%(self.client.name, self.project.name, self.pk, self.id_token, self.name)

  def update(self):
    for transcription in self.transcriptions.all():
      transcription.update()

    self.is_active = self.transcriptions.filter(is_active=True).count()!=0
    self.save()

  def process(self):
    '''
    Open relfile and create transcription objects.
    '''
    with open(os.path.join(self.csv_file.path, self.csv_file.file_name)) as open_relfile:
      lines = open_relfile.readlines()
      for i, line in enumerate(lines):
        print([self.name, 'line %d'%(i+1)])
        tokens = line.split('|') #this can be part of a relfile parser object with delimeter '|'
        transcription_audio_file_name = os.path.basename(tokens[0])
        confidence = tokens[2]
        utterance = tokens[3].strip() if ''.join(tokens[3].split()) != '' else ''
        value = tokens[4]
        confidence_value = tokens[5].rstrip() #chomp newline
        if confidence_value is not '':
          confidence_value = float(float(confidence_value)/1000.0) #show as decimal
        else:
          confidence_value = 0.0

        if self.wav_files.filter(file_name=transcription_audio_file_name).count()>0:
          #if .filter returns multiple files, take the first and delete the rest
          if self.wav_files.filter(file_name=transcription_audio_file_name).count()>1:
            for wav_file_i in self.wav_files.filter(file_name=transcription_audio_file_name):
              print(wav_file_i)
            wav_file = self.wav_files.filter(file_name=transcription_audio_file_name)[0]
            self.wav_files.filter(file_name=transcription_audio_file_name)[1:].delete()
          else:
            wav_file = self.wav_files.get(file_name=transcription_audio_file_name)

          transcription, created = self.transcriptions.get_or_create(client=self.client, project=self.project, wav_file__file_name=wav_file.file_name)

          transcription.wav_file = wav_file
          transcription.save()
          wav_file.save()

          if created:
            transcription.id_token = generate_id_token(Transcription)
            transcription.confidence = confidence
            transcription.utterance = utterance
            transcription.value = value
            transcription.confidence_value = confidence_value
            transcription.save()

    self.is_active = True
    self.save()

class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  grammar = models.ForeignKey(Grammar, related_name='transcriptions')
  job = models.ForeignKey(Job, null=True, related_name='transcriptions')

  #properties
  id_token = models.CharField(max_length=8)
  audio_file_data_path = models.CharField(max_length=255) #temporary
  audio_file = models.FileField(upload_to='audio')
  audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  audio_rms = models.CharField(max_length=255)
  confidence = models.CharField(max_length=255)
  utterance = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  confidence_value = models.DecimalField(max_digits=3, decimal_places=2, null=True)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  is_available = models.BooleanField(default=False)
  date_last_requested = models.DateTimeField(auto_now_add=False, null=True)
  latest_revision_done_by_current_user = models.BooleanField(default=False)

  #methods
  def __str__(self):
    return '%s > %s > %d:%s > %s'%(self.client.name, self.project.name, self.pk, self.id_token, self.utterance)

  def latest_revision_words(self):
    try:
      latest_revision = self.revisions.latest()
      return latest_revision.words.all()
    except ObjectDoesNotExist:
      return []

  def update(self):
    #if deactivation condition is satisfied, deactivate transcription
    self.is_active = not self.deactivation_condition()
    self.save()

  def deactivation_condition(self):
    ''' Has at least one revision with an utterance'''
    return (len(self.revisions.exclude(utterance=''))>0)

  def set_latest_revision_done_by_current_user(self, user):
    try:
      latest_revision = self.revisions.latest()
      self.latest_revision_done_by_current_user = (latest_revision.user.email==user.email and len(latest_revision.words.all())!=0)
      self.save()
    except ObjectDoesNotExist:
      pass

  def process(self):
    wav_file = self.grammar.wav_files.get(file_name=self.file_name)

    #1. process audio file -> IRREVERSIBLE
    (seconds, rms_values) = process_audio(self.wav_file.path)

    self.audio_time = seconds

    max_rms = max(rms_values)
    rms_values = [float(value)/float(max_rms) for value in rms_values]

    self.audio_rms = json.dumps(rms_values)

    #2. add open audio file to transcription
    with open(self.wav_file.path, 'rb') as open_audio_file:
      self.audio_file = File(open_audio_file)
      self.save()

    self.is_active = True
    self.is_available = True
    self.save()

  def unpack_rms(self):
    return [(int(rms*31+1), 32-int(rms*31+1)) for rms in json.loads(self.audio_rms)]

  def process_words(self):
    words = self.utterance.split()
    for word in words:
      unique = False
      tag = False
      if self.client.words.filter(project=self.project, char=word).count()==0:
        unique=True
      if '[' in word or ']' in word and ' ' not in word:
        tag = True

      self.words.create(client=self.client, project=self.project, grammar=self.grammar, char=word, unique=unique, tag=tag)

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')
  job = models.ForeignKey(Job, related_name='revisions')

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)
  utterance = models.CharField(max_length=255)

  ''' need to be determined by action_sequence() '''
  time_to_complete = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  number_of_plays = models.IntegerField(default=0)

  #methods
  def __str__(self):
    return '%s: "%s" modified to "%s" > by %s'%(self.id_token, self.transcription.utterance, self.utterance, self.user)

  def action_sequence(self):
    pass

  def process_words(self):
    words = self.utterance.split()
    self.words.all().delete()
    for word in words:
      unique = False
      tag = False
      if self.transcription.client.words.filter(project=self.transcription.project, char=word).count()==0:
        unique=True
      if '[' in word or ']' in word and ' ' not in word:
        tag = True

      self.words.create(client=self.transcription.client, project=self.transcription.project, grammar=self.transcription.grammar, transcription=self.transcription, char=word, unique=unique, tag=tag)

  #sorting
  class Meta:
    get_latest_by = 'date_created'

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')
  project = models.ForeignKey(Project, related_name='words')
  grammar = models.ForeignKey(Grammar, related_name='words')

  #properties
  id_token = models.CharField(max_length=8)
  char = models.CharField(max_length=255)
  unique = models.BooleanField(default=False) #marked as unique upon first occurence in a client.
  tag = models.BooleanField(default=False)

  #methods
  def __str__(self):
    return self.char

class TranscriptionWord(Word):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='words')

class RevisionWord(TranscriptionWord):
  #connections
  revision = models.ForeignKey(Revision, related_name='words')

class Action(models.Model): #lawsuit
  #types
  action_type_choices = (
    ('ea','ended audio'),
    ('r','replay'),
    ('pp','play pause'),
    ('a','add new word'),
    ('c','copy down'),
    ('t','tick'),
  )

  #connections
  client = models.ForeignKey(Client, related_name='actions')
  user = models.ForeignKey(User, related_name='actions')
  job = models.ForeignKey(Job, related_name='actions')
  transcription = models.ForeignKey(Transcription, related_name='actions')
  revision = models.ForeignKey(Revision, related_name='actions')

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)
  char = models.CharField(max_length=255, choices=action_type_choices, default='')
  audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True) #time at which the audio was skipped: next

  #methods
  def __str__(self):
    return '%s > %s > %s'%(self.job.id_token, self.user, self.char)

### File paths
class CSVFile(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='csv_files')
  project = models.ForeignKey(Project, related_name='csv_files')
  grammar = models.OneToOneField(Grammar, related_name='csv_file', null=True)

  #properties
  name = models.CharField(max_length=255)
  path = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)

  #methods
  def __str__(self):
    return '%s > %s > %s > %d:%s'%(self.client.name, self.project.name, self.grammar.name, self.pk, self.file_name)

class WavFile(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='wav_files')
  project = models.ForeignKey(Project, related_name='wav_files')
  grammar = models.ForeignKey(Grammar, related_name='wav_files')
  transcription = models.OneToOneField(Transcription, related_name='wav_file', null=True)

  #properties
  path = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)

  #methods
  def __str__(self):
    return '%s > %s > %s > %d:%s'%(self.client.name, self.project.name, self.grammar.name, self.pk, self.file_name)
