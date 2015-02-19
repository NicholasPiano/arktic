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
  client_path = models.TextField(max_length=255)

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

  def export(self):
    count = self.grammars.count()
    for i,g in enumerate(self.grammars.all()):
      print('%d/%d: %s' % (i+1, count, str(g)))
      g.export()

class Project(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='projects')

  #properties
  id_token = models.CharField(max_length=8)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=False)
  project_path = models.TextField(max_length=255)
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

  def process_grammars(self):
    '''
    Wrapper for processing done by grammars.
    '''
    print('processing grammars...')
    count = self.grammars.count()
    for i, grammar in enumerate(self.grammars.all()):
      print('grammar %d/%d'%(i+1, count), end='\r' if i<count-1 else '\n')
      grammar.process()

  def process_transcriptions(self):
    '''
    Wrapper for individual processing done by transcriptions.
    '''
    print('processing transcriptions...')
    count = self.transcriptions.count()
    for i, transcription in enumerate(self.transcriptions.all()):
      print('transcription %d/%d'%(i+1, count), end='\r' if i<count-1 else '\n')
      transcription.process()

  def process_words(self):
    '''
    Wrapper for transcription word processing.
    '''
    print('processing words...')
    count = self.transcriptions.count()
    for i, transcription in enumerate(self.transcriptions.all()):
      print('words %d/%d'%(i+1, count), end='\r' if i<count-1 else '\n')
      transcription.process_words()

  def create_jobs(self):
    '''
    Create all possible jobs from the set of transcriptions.
    '''
    if self.jobs.count()==0:
      print('creating jobs...')
      filter_set = self.transcriptions.filter(is_available=True).order_by('grammar__name')
      counter = filter_set.count() - 1 if filter_set.count() else 0
      while counter:
        print('available: %d'%(counter), end='\r')
        job = self.jobs.create(client=self.client, id_token=generate_id_token(Job))
        lower_bound = counter-settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB if counter>=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB else 0
        job_set = filter_set[lower_bound:counter]
        job.get_transcription_set(job_set)
        job.save()
        counter = lower_bound
      print('available: 0')

class Job(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='jobs', null=True)
  project = models.ForeignKey(Project, related_name='jobs', null=True)
  user = models.ForeignKey(User, related_name='jobs', null=True)

  #properties
  is_active = models.BooleanField(default=True)
  is_available = models.BooleanField(default=True)
  id_token = models.CharField(max_length=8) #a random string of characters to identify the job
  active_transcriptions = models.IntegerField(editable=False, default=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
  date_created = models.DateTimeField(auto_now_add=True)
  date_completed = models.DateTimeField(auto_now_add=False, null=True)
  total_transcription_time = models.DecimalField(max_digits=8, decimal_places=5, null=True)
  time_taken = models.DecimalField(max_digits=8, decimal_places=6, null=True)

  #methods
  def __str__(self):
    return str(self.project) + ' > ' + str(self.user) + ', job ' + str(self.pk) + ':' + str(self.id_token)

  def get_transcription_set(self, job_set):
    self.active_transcriptions = len(job_set)

    ''' total_transcription_time variable '''

    for transcription in job_set:
      transcription.date_last_requested = timezone.now()
      transcription.is_available = False
      self.transcriptions.add(transcription)
      transcription.save()

    #set total_transcription_time
    self.total_transcription_time = float(sum([float(t.audio_time) for t in self.transcriptions.all()]))

  def update(self): #not used for export. Just for recording values.
    ''' active_transcriptions, time_taken '''

    for transcription in self.transcriptions.all():
      transcription.update()

    self.active_transcriptions = self.transcriptions.filter(is_active=True).count()
    if self.active_transcriptions==0:
      self.is_active = False
      self.date_completed = timezone.now()

    time_taken = 0
    for transcription in self.transcriptions.filter(is_active=False):
      #get total time for current user
      for revision in transcription.revisions.filter(user=self.user):
        time_taken += revision.time_to_complete if revision.time_to_complete else 0
    self.time_taken = time_taken

    self.save()
