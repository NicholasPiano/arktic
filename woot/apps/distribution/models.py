#woot.apps.distribution.models

#django
from django.db import models

#local
from apps.users.models import User

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
  def update(self):
    '''

    Update is called when a revision is submitted. This will propagate down the chain:
    Client > Project > Relfile > Transcription

    When a relfile is completed, a completed_relfile object will be created from the chosen revisions.
    When a project is completed, a completed_project object will be created. This will be available for
    download from the admin in the form of a zip file.

    '''

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
    ''' Updates project when a revision is submitted. '''

  def export(self):
    ''' Export prepares all of the individual relfiles to be packaged and be available for download. '''

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

class Word(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='words')
  project = models.ForeignKey(Project, related_name='words')
  relfile = models.ForeignKey(Relfile, related_name='words')

  #properties
  char = models.CharField(max_length=255)
  unique = models.BooleanField(default=False) #marked as unique upon first occurence in a client.

  #methods
  def __unicode__(self):


### ACTIONS
class Action(models.Model):
  #connections
  job = models.ForeignKey(Job, related_name='actions')
  user = models.ForeignKey(User, related_name='actions')

  #properties
  date_created = models.DateTimeField(auto_now_add=True)

class NewJobAction

new job
ended audio
previous
next
replay
play pause
add new word
copy down
tick
