#woot.apps.distribution.models

#django
from django.db import models

#local

#util

#vars

#classes
class Client(models.Model):
  #connections
  #sub: projects, jobs, archives, relfiles, transcriptions, autocomplete words

  #properties
  name = models.CharField(max_length=255)

  #methods
  def __unicode__(self):

  #custom methods
  def create_autocomplete_words(self):
  def update(self):

class Project(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='projects')
  #sub: jobs, archives, relfiles, transcriptions

  #properties
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)

  #methods
  def __unicode__(self):

  #custom methods
  def update(self):
  def export(self):

class CompletedProject(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='completed_projects')

  #properties
  name = models.CharField(max_length=255)
  archive_file = models.FileField(upload_to='completed', null=True, max_length=255)

  #methods
  def __unicode__(self):

class Job(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='jobs')
  project = models.ForeignKey(Project, related_name='jobs')
  user = models.ForeignKey(User, related_name='jobs')
  #sub: transcriptions (null)

  #properties
  is_active = models.BooleanField(default=True)
  active_transcriptions = models.IntegerField(editable=False)
  total_transcription_time = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, editable=False)
  date_created = models.DateTimeField(auto_now_add=True)
  time_taken = models.DecimalField(max_digits=5, decimal_places=1, default=0.0, editable=False)

  #methods
  def __unicode__(self):

  #custom methods
  def get_transcription_set(self):
  def update(self):

class Action(models.Model):
  #connections
  job = models.ForeignKey(Job, related_name='actions')
  user = models.ForeignKey(User, related_name='actions')

  #properties
  button_id = models.CharField(max_length=100)
  transcription_id = models.CharField(max_length=100)
  transcription_utterance = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):

  #custom methods

class AutocompleteWord(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')

  #properties
  char = models.CharField(max_length=255)

  #methods
  def __unicode__(self):
