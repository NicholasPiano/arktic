#woot.apps.distribution.models

#django
from django.db import models

#local
from apps.users.models import User

#util
import os
import zipfile as zp
import shutil as sh
import datetime as dt

#vars

#classes
class Client(models.Model):
  #properties
  name = models.CharField(max_length=255)
  client_path = models.CharField(max_length=255)

  #methods
  def __str__(self):
    return self.name

  def update(self):
    '''

    Update is called when a revision is submitted. This will propagate down the chain:
    Client > Project > Grammar > Transcription

    When a relfile is completed, a completed_relfile object will be created from the chosen revisions.
    When a project is completed, a completed_project object will be created. This will be available for
    download from the admin in the form of a zip file.

    '''
    for project in self.projects.filter(is_active=True, is_approved=True):
      project.update()
      if not project.is_active:
        project.export()

class Project(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='projects')

  #properties
  id_token = models.CharField(max_length=8)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  is_new = models.BooleanField(default=True)
  is_approved = models.BooleanField(default=False)
  completed_project_file = models.FileField(upload_to='completed_projects')

  #methods
  def __str__(self):
    return str(client) + ' > ' + str(self.name)

  def update(self):
    ''' Updates project when a revision is submitted. '''
    for grammar in self.grammars.filter(is_active=True):
      grammar.update()
      if not grammar.is_active:
        grammar.export()

    #update status: approved, new, active

  def export(self):
    ''' Export prepares all of the individual relfiles to be packaged and be available for download. '''
    pass

class Job(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='jobs')
  project = models.ForeignKey(Project, related_name='jobs')
  user = models.ForeignKey(User, related_name='jobs')

  #properties
  is_active = models.BooleanField(default=True)
  id_token = models.CharField(max_length=8) #a random string of characters to identify the job
  project_path = models.CharField(max_length=255)
  active_transcriptions = models.IntegerField(editable=False)
  date_created = models.DateTimeField(auto_now_add=True)
  total_transcription_time = models.DateTimeField(auto_now_add=False, null=True)
  time_taken = models.DateTimeField(auto_now_add=False, null=True)

  #methods
  def __str__(self):
    return str(self.project) + ' > ' + str(self.user) + ', job ' + str(self.pk) + ':' + str(self.id_token)

  def get_transcription_set(self):
    project_transcriptions = self.project.transcriptions.filter(is_active=True).order_by('utterance')
    transcription_set = project_transcriptions[-NUMBER_OF_TRANSCRIPTIONS_PER_JOB:] if len(project_transcriptions)>NUMBER_OF_TRANSCRIPTIONS_PER_JOB else project_transcriptions

    ''' total_transcription_time variable '''

    for transcription in transcription_set:
      transcription.date_last_requested = dt.datetime.now()
      transcription.save()
      self.transcriptions.add(transcription)

    #set total_transcription_time

    self.save()

  def update(self): #not used for export. Just for recording values.
    ''' active_transcriptions, time_taken '''

    self.active_transcriptions = self.transcriptions.filter(is_active=True).count()

    time_taken = 0
    for transcription in self.transcriptions.filter(is_active=False):
      #get total time for current user
      for revision in transcription.revisions.filter(user=user):
        time_taken += revision.time_to_complete
    self.time_taken = time_taken

    self.save()

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
  rel_file_path = models.CharField(max_length=255, null=True)
  complete_rel_file = models.FileField(upload_to='completed')

  #methods
  def __str__(self):
    return '%s > %s > %d:%s > %s'%(self.client.name, self.project.name, self.pk, self.id_token, self.name)
  def update(self):
    pass
  def extract(self, rel_file_path):
    pass
