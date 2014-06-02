#transcription.models

#django
from django.core.files import File
from django.db import models
from django.db.models.fields.files import FileField

#local
# from transcription.fields import AudioField
from transcription.base_model import Model
from arktic.settings import MEDIA_ROOT
from users.models import Employee as User
from distribution.models import Job, Distributor

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
transcription_types = [
    'yes-no',
]

class Transcription(Model):
    #connections
    distributor = models.ForeignKey(Distributor, related_name='transcriptions')
    users = models.ManyToManyField(User)
    jobs = models.ManyToManyField(Job)

    #properties
    type = models.CharField(max_length=100)
    audio_file = FileField(upload_to='audio', max_length=255) #use audiofield when done
    grammar = models.CharField(max_length=255)
    confidence = models.CharField(max_length=255)
    utterance = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    confidence_value = models.DecimalField(max_digits=20, decimal_places=9)
    requests = models.IntegerField(default=0) #number of times the transcription has been requested.
    add_date = models.DateTimeField(auto_now_add=True)
    date_last_requested = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        if kwargs:
            #modify keywords
            #-grammar
            kwargs['grammar'] = os.path.splitext(os.path.basename(kwargs['grammar']))[0] #just get grammar name
            #-confidence_value
            confidence_value = kwargs['confidence_value'].rstrip() #chomp newline
            if confidence_value is not '':
                kwargs['confidence_value'] = float(float(confidence_value)/1000.0) #show as decimal
            else:
                kwargs['confidence_value'] = 0.0

        super(Transcription, self).__init__(*args, **kwargs)
#         self.audio_file.file.close()

    def __unicode__(self):
        return self.utterance

    #save - always called by 'create'
    def save(self, *args, **kwargs):
        super(Transcription, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.audio_file.delete(save=False)
        super(Transcription, self).delete(*args, **kwargs)

class Revision(models.Model):
    #connections
    transcription = models.ForeignKey(Transcription, related_name='revisions')

    #properties

