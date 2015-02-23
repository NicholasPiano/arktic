#apps.transcription.models

#django
from django.db import models
from django.core.files import File
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings

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

    self.is_active = self.transcriptions.filter(is_active=True).count()>0
    self.save()

  def process(self):
    '''
    Open relfile and create transcription objects.
    '''
    if self.transcriptions.count()==0:
      with open(os.path.join(self.csv_file.path, self.csv_file.file_name)) as open_relfile:
        lines = open_relfile.readlines()
        for i, line in enumerate(lines):
          print('%s: line %d/%d' % (self.name, i+1, len(lines)), end='\r' if i<len(lines)-1 else '\n')
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
              transcription.id_token = str(transcription.pk)
              transcription.confidence = confidence
              transcription.utterance = utterance
              transcription.value = value
              transcription.confidence_value = confidence_value
              transcription.save()

      self.is_active = True
      self.save()

  def export(self):
    '''

    Sample line in relfile that needs to be reproduced:
    ./2014/10October/01/bshoscar22PCI/311-150-10012014-133918231-20141001134132.wav|c:\\Program Files\\Nortel\\PERIsw30r\\grammars\\927-London.grxml|ok|neasden station|{borough:BRENT borough_code:B0004 code:S0304 location:NEASDEN nhs_code:5K5}|762
    1. ./2014/10October/01/bshoscar22PCI/311-150-10012014-133918231-20141001134132.wav | (audio file path)
    2. c:\\Program Files\\Nortel\\PERIsw30r\\grammars\\927-London.grxml | (grammar name)
    3. ok | (confidence)
    4. neasden station | (utterance)
    5. {borough:BRENT borough_code:B0004 code:S0304 location:NEASDEN nhs_code:5K5} | (value?)
    6. 762 (confidence value)

    How to obtain details from database:
    1. transcription.wav_file.path:

    path = transcription.wav_file.path
    path = './' + path[path.index('2014')]

    2. transcription.grammar.name
    3. transcription.confidence
    4. transcription.revisions.latest().utterance
    5. transcription.value
    6. float(transcription.confidence_value)

    '''
    completed_dir = os.path.join(settings.MEDIA_ROOT, 'completed', self.client.name)

    if not os.path.exists(completed_dir):
      os.mkdir(completed_dir)

    with open(os.path.join(completed_dir, '%s.csv'%self.name), 'w+') as csv_file:
      for t in self.transcriptions.all():
        csv_file.write(t.line())

class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  grammar = models.ForeignKey(Grammar, related_name='transcriptions')
  job = models.ManyToManyField(Job, related_name='transcriptions', null=True)

  #properties
  id_token = models.CharField(max_length=8)
  audio_file_data_path = models.CharField(max_length=255) #temporary
  audio_file = models.FileField(upload_to='audio')
  audio_time = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  audio_rms = models.TextField()
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
    return '%s > %s > %d:%s > "%s"'%(self.client.name, self.project.name, self.pk, self.id_token, self.utterance)

  def line(self):
    path = self.wav_file.path
    path = './' + path[path.index('2014'):]
    return '%s|%s|%s|%s|%s|%d\n' % (path, self.grammar.csv_file.file_name, self.confidence, self.revisions.latest().utterance, self.value, int(1000*float(self.confidence_value)) if self.confidence_value else 0)

  def grammar_name(self):
    return self.grammar.name if len(self.grammar.name)<50 else self.grammar.name[:46] + '...'

  def latest_revision_words(self):
    try:
      latest_revision = self.revisions.latest()
      return latest_revision.split_utterance()
    except ObjectDoesNotExist:
      return []

  def update(self):
    #if deactivation condition is satisfied, deactivate transcription
    self.is_active = not self.deactivation_condition()
    self.save()

  def deactivation_condition(self):
    ''' Has at least one revision with an utterance'''
    return (self.revisions.exclude(utterance='').count()>0)

  def set_latest_revision_done_by_current_user(self, user):
    if self.revisions.count()>0:
      latest_revision = self.revisions.latest()
      self.latest_revision_done_by_current_user = (latest_revision.user.email==user.email and latest_revision.utterance!='')
    else:
      self.latest_revision_done_by_current_user = False
    self.save()

  def process(self):
    #1. process audio file -> IRREVERSIBLE
    if len(self.audio_rms)<10:
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
    if self.words.count()==0:
      words = self.utterance.split()
      for word in words:
        tag = ('[' in word or ']' in word)

        #many to many relationship
        if tag and not (('[' in word and ']' not in word) or (']' in word and '[' not in word)):
          w, created = self.project.words.get_or_create(char=word) #unique by char to project
          if created:
            w.client = self.client
            w.grammar = self.grammar
            w.id_token = generate_id_token(Word)
            w.tag = True
            self.words.add(w)
            w.save()

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

  def split_utterance(self):
    return self.utterance.split(' ')

  def action_sequence(self):
    pass

  def process_words(self):
    words = self.utterance.split()
    for word in words:
      #many to many relationship
      if not (('[' in word and ']' not in word) or (']' in word and '[' not in word)): #reject with only one bracket
        w, created = self.job.project.words.get_or_create(char=word) #unique by char to project
        if created:
          w.client = self.transcription.client
          w.grammar = self.transcription.grammar
          w.id_token = generate_id_token(Word)
          w.tag = ('[' in word and ']' in word)

        self.words.add(w)
        w.save()

  def process_actions(self):
    for action in self.job.actions.filter(transcription=self.transcription):
      self.actions.add(action)
      action.save()

  #sorting
  class Meta:
    get_latest_by = 'date_created'

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words', null=True)
  project = models.ForeignKey(Project, related_name='words')
  grammar = models.ForeignKey(Grammar, related_name='words', null=True)
  transcription = models.ManyToManyField(Transcription, related_name='words')
  revision = models.ManyToManyField(Revision, related_name='words')

  #properties
  id_token = models.CharField(max_length=8)
  char = models.CharField(max_length=255)
  tag = models.BooleanField(default=False)

  #methods
  def __str__(self):
    return self.char

class Action(models.Model): #lawsuit
  #connections
  client = models.ForeignKey(Client, related_name='actions')
  user = models.ForeignKey(User, related_name='actions')
  job = models.ForeignKey(Job, related_name='actions')
  transcription = models.ForeignKey(Transcription, related_name='actions')
  revision = models.ForeignKey(Revision, related_name='actions', null=True)

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)
  char = models.CharField(max_length=255, default='')
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
  path = models.TextField(max_length=255)
  file_name = models.TextField(max_length=255)

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
  path = models.TextField(max_length=255)
  file_name = models.TextField(max_length=255)

  #methods
  def __str__(self):
    return '%s > %s > %s > %d:%s'%(self.client.name, self.project.name, self.grammar.name, self.pk, self.file_name)
