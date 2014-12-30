#woot.apps.transcription.models

#django
from django.db import models

#local
from apps.distribution.models import Client, Project, Job, Grammar
from apps.users.models import User

#util
from datetime import datetime as dt

#vars

#classes
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
  audio_time = models.DateTimeField(auto_now_add=False, null=True)
  confidence = models.CharField(max_length=255)
  utterance = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  date_last_requested = models.DateTimeField(auto_now_add=False, null=True)

  #methods
  def __str__(self):
    return '%s > %s > %d:%s > %s'%(self.client.name, self.project.name, self.pk, self.id_token, self.utterance)
  def latest_revision_words(self):
    pass
  def update(self):
    pass
  def latest_revision_done_by_current_user(self):
    pass
  def process(self):
    #1. process audio file
    #2. add open audio file to transcription
    pass

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')

  #properties
  id_token = models.CharField(max_length=8)
  date_created = models.DateTimeField(auto_now_add=True)

  ''' need to be determined by action_sequence() '''
  time_to_complete = models.DateTimeField(auto_now_add=False)
  number_of_plays = models.IntegerField(default=0)

  #methods
  def __str__(self):
    pass
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

  #methods
  def __str__(self):
    pass

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

class WavFile(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='wav_files')
  project = models.ForeignKey(Project, related_name='wav_files')
  grammar = models.ForeignKey(Grammar, related_name='wav_files', null=True)
  transcription = models.OneToOneField(Transcription, related_name='wav_file', null=True)

  #properties
  path = models.CharField(max_length=255)
  file_name = models.CharField(max_length=255)
