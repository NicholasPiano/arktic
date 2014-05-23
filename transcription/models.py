#django
from django.core.files import File
from django.contrib.auth.models import User

#local
from archive.models import Archive
# from transcription.fields import AudioField
# from transcription.base_model import Model
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


