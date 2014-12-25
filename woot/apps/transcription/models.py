#woot.apps.transcription.models

#django
from django.db import models

#local
from apps.distribution.models import Client, Project, Job

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
  def __unicode__(self):
  def update(self):

class Archive(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='archives')

  #properties
  file = ContentTypeRestrictedFileField(upload_to='archives', max_length=255, content_types=['application/zip'])
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __unicode__(self):
  def extract(self):

class RelFile(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='relfiles')

  #properties
  rel_file = models.FileField(upload_to='relfiles', max_length=255)
  name = models.CharField(max_length=255)
  language = models.CharField(max_length=3)
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __unicode__(self):
  def extract(self):

class CompletedRelFile(models.Model):
  #connections
  grammar = models.ForeignKey(Grammar, related_name='completed_relfiles')

  #properties
  file = models.FileField(upload_to='completed', max_length=255)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __unicode__(self):

class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  grammar = models.ForeignKey(Grammar, related_name='transcriptions')
  job = models.ForeignKey(Job, null=True, related_name='transcriptions')

  #properties
  audio_file = FileField(upload_to='audio', max_length=255)
  audio_time = models.DateTimeField(auto_now_add=False)
  confidence = models.CharField(max_length=255)
  utterance = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  #methods
  def __unicode__(self):
  def latest_revision_words(self):
  def update(self):
  def latest_revision_done_by_current_user(self):
  def date_last_requested(self):

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
  def __unicode__(self):
  def action_sequence(self):

  #sorting
  class Meta:
    get_latest_by = 'date_created'

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')
  project = models.ForeignKey(Project, related_name='words')
  relfile = models.ForeignKey(Relfile, related_name='words')
  transcription = models.ForeignKey(Transcription, related_name='words')

  #properties
  char = models.CharField(max_length=255)
  unique = models.BooleanField(default=False) #marked as unique upon first occurence in a client.

  #methods
  def __unicode__(self):

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
    ('r','replay')
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
  date_created = models.DateTimeField(auto_now_add=True)
  char = models.CharField(max_length=255, choices=action_type_choices, default='')

  #methods
  def __unicode__(self):
    pass
