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

  #methods
  def __unicode__(self):
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
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  is_approved = models.BooleanField(default=False)

  #methods
  def __unicode__(self):
    return unicode(client) + ' > ' + unicode(self.name)

  def update(self):
    ''' Updates project when a revision is submitted. '''
    for grammar in self.grammars.filter(is_active=True):
      grammar.update()
      if not grammar.is_active:
        grammar.export()

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
  active_transcriptions = models.IntegerField(editable=False)
  total_transcription_time = models.DateTimeField(auto_now_add=False)
  date_created = models.DateTimeField(auto_now_add=True)
  time_taken = models.DateTimeField(auto_now_add=False)

  #methods
  def __unicode__(self):
    return unicode(self.project) + ' > ' + unicode(self.user) + ', job ' + unicode(self.pk) + ':' + unicode(self.id_token)

  def get_transcription_set(self):
    project_transcriptions = self.project.transcriptions.filter(is_active=True).order_by('utterance')
    transcription_set = project_transcriptions[-NUMBER_OF_TRANSCRIPTIONS_PER_JOB:] if len(project_transcriptions)>NUMBER_OF_TRANSCRIPTIONS_PER_JOB else project_transcriptions

    for transcription in transcription_set:
      transcription.date_last_requested = dt.datetime.now()
      transcription.save()
      self.transcriptions.add(transcription)

  def update(self): #not used for export. Just for recording values.
    pass
