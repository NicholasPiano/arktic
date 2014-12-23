#woot.apps.transcription.models

#django
from django.db import models

#local

#util

#vars

#classes
class Archive(models.Model):
  #connections
  project = models.ForeignKey(Project, related_name='archives')
  #sub: relfiles, transcriptions

  #properties
  archive_file = ContentTypeRestrictedFileField(upload_to='archive', max_length=255, content_types=['application/zip'])
  date_created = models.DateTimeField(auto_now_add=True)

  #methods
  def __unicode__(self):

  #override methods
  def save(self, *args, **kwargs):
    if self.pk is None:
      super(Archive, self).save(*args, **kwargs)
      self.extract() #necessary here because this is done through the admin. When I write an upload view, this will not be necessary.
    else:
      super(Archive, self).save(*args, **kwargs) #first time

  #custom methods
  def extract(self):

class RelFile(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='relfiles')
  project = models.ForeignKey(Project, related_name='relfiles')
  archive = models.ForeignKey(Archive, related_name='relfiles')
  #sub: transcriptions, autocomplete words

  #properties
  is_active = models.BooleanField(default=True)
  rel_file = models.FileField(upload_to='relfiles', max_length=255)
  name = models.CharField(max_length=255)
  language = models.CharField(max_length=3, choices=language_choices, default=english)
  date_created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):

  #custom methods
  def update(self):
  def extract(self, inner_zip_path=None, file_dictionary=None, index=None):

class CompletedRelFile(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='completed_relfiles')
  project = models.ForeignKey(Project, related_name='completed_relfiles')
  archive = models.ForeignKey(Archive, related_name='completed_relfiles')
  relfile = models.ForeignKey(RelFile, related_name='completed_relfiles')
  #sub: transcriptions (null)

  #properties
  completed_rel_file = models.FileField(upload_to='completed_relfiles', max_length=255)
  name = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):

  #custom methods

class Transcription(models.Model):
  #connections
  client = models.ForeignKey(Client, related_name='transcriptions')
  project = models.ForeignKey(Project, related_name='transcriptions')
  archive = models.ForeignKey(Archive, related_name='transcriptions')
  job = models.ForeignKey(Job, null=True, related_name='transcriptions')
  relfile = models.ForeignKey(RelFile, related_name='transcriptions')
  #sub: transcription words, revisions

  #properties
  audio_file = FileField(upload_to='audio', max_length=255) #use audiofield when done
  line_number = models.IntegerField()
  time = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
  grammar = models.CharField(max_length=255)
  confidence = models.CharField(max_length=255)
  utterance = models.CharField(max_length=255)
  value = models.CharField(max_length=255)
  confidence_value = models.DecimalField(max_digits=3, decimal_places=2)
  requests = models.IntegerField(default=0) #number of times the transcription has been requested.
  add_date = models.DateTimeField(auto_now_add=True)
  date_last_requested = models.DateTimeField(auto_now_add=True)
  is_active = models.BooleanField(default=True)
  latest_revision_done_by_current_user = models.BooleanField(default=False)

  def __unicode__(self):

  #custom methods
  def latest_revision_words(self, user):

class TranscriptionWord(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='words')

  #properties
  content = models.CharField(max_length=255)

  def __unicode__(self):

class Revision(models.Model):
  #connections
  transcription = models.ForeignKey(Transcription, related_name='revisions')
  user = models.ForeignKey(User, related_name='revisions')
  #sub: revision words

  #properties
  utterance = models.CharField(max_length=255)
  date_created = models.DateTimeField(auto_now_add=True)

  def __unicode__(self):

  class Meta:
    get_latest_by = 'date_created'


class RevisionWord(models.Model):
  #connections
  revision = models.ForeignKey(Revision, related_name='words')

  #properties
  content = models.CharField(max_length=255)

  def __unicode__(self):
