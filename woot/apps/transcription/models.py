#woot.apps.transcription.models

#django
from django.db import models
from django.core.files import File

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
  is_processed = models.BooleanField(default=False)
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
    self.is_active = True
    for transcription in self.transcriptions.all():
      transcription.update()
      if self.is_active:
        self.is_active = transcription.is_active
    self.save()

  def process(self):
    '''
    Open relfile and create transcription objects.
    '''
    with open(os.path.join(self.csv_file.path, self.csv_file.file_name)) as open_relfile:
      lines = open_relfile.readlines()
      for line in lines:
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

        if self.wav_files.filter(file_name=transcription_audio_file_name)!=[]:

          #if .filter returns multiple files, take the first and delete the rest
          if len(self.wav_files.filter(file_name=transcription_audio_file_name))>1:
            for wav_file_i in self.wav_files.filter(file_name=transcription_audio_file_name):
              print(wav_file_i)
            wav_file = self.wav_files.filter(file_name=transcription_audio_file_name)[0]
            self.wav_files.filter(file_name=transcription_audio_file_name)[1:].delete()

          else:
            wav_file = self.wav_files.get(file_name=transcription_audio_file_name)

          transcription, created = self.transcriptions.get_or_create(client=self.client, project=self.project, wav_file__file_name=wav_file.file_name)

          if created:
            transcription.wav_file = wav_file
            transcription.id_token = generate_id_token(Transcription)
            transcription.confidence = confidence
            transcription.utterance = utterance
            transcription.value = value
            transcription.confidence_value = confidence_value
            transcription.save()
            wav_file.save()
            transcription.process()

    self.is_processed = True
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
  is_active = models.BooleanField(default=True)
  is_processed = models.BooleanField(default=False)
  date_last_requested = models.DateTimeField(auto_now_add=False, null=True)

  #methods
  def __str__(self):
    return '%s > %s > %d:%s > %s'%(self.client.name, self.project.name, self.pk, self.id_token, self.utterance)

  def latest_revision_words(self):


  def update(self):
    #if deactivation condition is satisfied, deactivate transcription
    if self.deactivation_condition():
      self.is_active = False
    self.save()

  def deactivation_condition(self):
    ''' Has at least one revision '''
    return (len(self.revisions.all())>0)

  def latest_revision_done_by_current_user(self, user):
    #1. get latest revision
    latest_revision = self.latest_revision()
    return latest_revision.user==user

  def latest_revision(self):
    return self.revisions.order_by('date_created')[0]

  def process(self):
    #1. process audio file -> IRREVERSIBLE
    (seconds, rms_values) = process_audio(self.wav_file.path)

    self.audio_time = seconds
    self.audio_rms = json.dumps(rms_values)

    #2. add open audio file to transcription
    with open(self.wav_file.path, 'rb') as open_audio_file:
      self.audio_file = File(open_audio_file)
      self.save()

    #3. add words to transcription
    for utterance_word in self.utterance.split(' '):
      word = self.words.create(client=self.client, project=self.project, grammar=self.grammar, char=utterance_word)

      word.id_token = generate_id_token(Word)
      if '[' in utterance_word or ']' in utterance_word: #tag
        word.tag = True
      if len(self.client.words.filter(char=word.char))<2:
        word.unique = True

      word.save()

    self.is_active = True
    self.is_processed = True
    self.save()

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)
  utterance = models.CharField(max_length=255)

  ''' need to be determined by action_sequence() '''
  time_to_complete = models.DecimalField(max_digits=8, decimal_places=6, null=True)
  number_of_plays = models.IntegerField(default=0)

  #methods
  def __str__(self):
    return 'transcription %d:%s modified to %s > by %s'%(self.transcription.pk, self.transcription.utterance, self.utterance, self.user)
  def action_sequence(self):
    pass

  #sorting
  class Meta:
    get_latest_by = 'date_created'

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')
  project = models.ForeignKey(Project, related_name='words')
  grammar = models.ForeignKey(Grammar, related_name='words')
  transcription = models.ForeignKey(Transcription, related_name='words')

  #properties
  id_token = models.CharField(max_length=8)
  char = models.CharField(max_length=255)
  unique = models.BooleanField(default=False) #marked as unique upon first occurence in a client.
  tag = models.BooleanField(default=False)

  #methods
  def __str__(self):
    return self.char

class RevisionWord(Word):
  #connections
  revision = models.ForeignKey(Revision, related_name='words')

class Action(models.Model): #lawsuit
  #types
  action_type_choices = (
    ('nj','new job'),
    ('ea','ended audio'),
    ('p','previous'),
    ('n','next'),
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
    return 'job %d > %s > %s'%(self.job.pk, self.user, self.char)

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
