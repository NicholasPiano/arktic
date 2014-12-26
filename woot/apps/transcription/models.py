#woot.apps.transcription.models

#django
from django.db import models

#local
from apps.distribution.models import Client, Project, Job
from apps.users.models import User

#util

#vars

#classes
class Grammar(models.Model):
  ''' Stores all information about a single grammar: relfile, archive, transcriptions '''
  #connections
  client = models.ForeignKey(Client, related_name='grammars')
  project = models.ForeignKey(Project, related_name='grammars')

  #properties
  is_active = models.BooleanField(default=True)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  date_completed = models.DateTimeField(auto_now_add=False)

  #methods
  def __str__(self):
    pass
  def update(self):
    pass

class Archive(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='archives')

  #properties
  file = models.FileField(upload_to='archives')
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __str__(self):
    pass
  def extract(self):
    pass

class RelFile(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='relfiles')

  #properties
  rel_file = models.FileField(upload_to='relfiles', max_length=255)
  name = models.CharField(max_length=255)
  language = models.CharField(max_length=3)
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __str__(self):
    pass
  def extract(self):
    pass

class CompletedRelFile(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='completed_relfiles')

  #properties
  file = models.FileField(upload_to='completed', max_length=255)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __str__(self):
    pass

class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  grammar = models.ForeignKey(Grammar, related_name='transcriptions')
  job = models.ForeignKey(Job, null=True, related_name='transcriptions')

  #properties
  audio_file = models.FileField(upload_to='audio')
  audio_time = models.DateTimeField(auto_now_add=False)
  confidence = models.CharField(max_length=255)
  utterance = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  date_last_requested = models.DateTimeField(auto_now_add=False)

  #methods
  def __str__(self):
    pass
  def latest_revision_words(self):
    pass
  def update(self):
    pass
  def latest_revision_done_by_current_user(self):
    pass

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')

  #properties
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
    'new job',
    'ended audio',
    'previous',
    'next',
    'replay',
    'play pause',
    'add new word',
    'copy down',
    'tick',
  )

  #connections
  client = models.ForeignKey(Client, related_name='actions')
  user = models.ForeignKey(User, related_name='actions')
  job = models.ForeignKey(Job, related_name='actions')
  transcription = models.ForeignKey(Transcription, related_name='actions')
  revision = models.ForeignKey(Revision, related_name='actions')

  #properties
  date_created = models.DateTimeField(auto_now_add=True)
  char = models.CharField(max_length=255, choices=action_type_choices, default='')

  #methods
  def __str__(self):
    pass
