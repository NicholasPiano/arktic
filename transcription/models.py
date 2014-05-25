#django
from django.core.files import File
from django.contrib.auth.models import User
from django.db import models
from django.db.models.fields.files import FileField

#local
from archive.models import Archive
# from transcription.fields import AudioField
from transcription.base_model import Model
from arktic.settings import MEDIA_ROOT

#third party


#util
import wave as wv
import numpy as np
import os
import subprocess as sp

#class vars
WAV_TYPE = 'wav'
ORIGINAL_AUDIO_ROOT = os.path.join(MEDIA_ROOT, 'original_audio')
WAV_ROOT = os.path.join(MEDIA_ROOT, WAV_TYPE)

#main transcription model
class Transcription(Model):
    #properties
    archive = models.ForeignKey(Archive, related_name='transcriptions', editable=False)
    audio_file = FileField(upload_to='audio', max_length=255, editable=False)
    column2 = models.CharField(max_length=255)
    column3 = models.CharField(max_length=255)
    utterance = models.CharField(max_length=255)
    column5 = models.CharField(max_length=255)
    column6 = models.CharField(max_length=255)

    def __unicode__(self):
        return self.utterance

    #save - always called by 'create'
    def save(self, *args, **kwargs):
        super(Transcription, self).save(*args, **kwargs)
        #1. ensure file is .wav
        #2.

    def delete(self, *args, **kwargs):
        self.audio_file.delete(save=False)
        super(RelFile, self).delete(*args, **kwargs)
