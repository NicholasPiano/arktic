#woot.apps.distribution.models

#django
from django.db import models
from django.conf import settings
from django.utils import timezone

#local
from apps.users.models import User
from libs.utils import generate_id_token

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

class Project(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='projects')

  #properties
  id_token = models.CharField(max_length=8)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  project_path = models.CharField(max_length=255)
  completed_project_file = models.FileField(upload_to='completed_projects')

  #methods
  def __str__(self):
    return str(self.client) + ' > ' + str(self.name)

  def update(self):
    ''' Updates project when a revision is submitted. '''
    for job in self.jobs.filter(is_active=True):
      job.update()

    for grammar in self.grammars.filter(is_active=True):
      grammar.update()

    #update status: active, processed
    self.is_active = (self.jobs.filter(is_active=True).count()!=0 and self.grammars.filter(is_active=True).count()!=0)
    self.save()

  def export(self):
    ''' Export prepares all of the individual relfiles to be packaged and be available for download. '''
    pass

  def create_jobs(self):
    available_transcriptions = self.transcriptions.filter(is_available=True).count()
    while available_transcriptions>0:
      job = self.jobs.create(client=self.client, id_token=generate_id_token(Job))
      job.get_transcription_set()
