#django
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File

#local
from apps.transcription.models import Grammar, Transcription, Word
from apps.distribution.models import Project

#util
import json
import os

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    path_server = '/home/arkaeologic/arktic/woot/data/'
    path_down = '/Users/nicholaspiano/code/arktic/woot/data/'

#     self.stdout.write('processing transcriptions...')
    count = Transcription.objects.count()
    for i, t in enumerate(Transcription.objects.all()):
      print(['audio', i+1, count, t.pk])

      #1. replace path of transcription.wav_file with server path
      if 'nicholaspiano' in t.wav_file.path:
        t.wav_file.path = os.path.join(path_server, t.wav_file.path[len(path_down):])
        t.wav_file.save()

      #2. open new path and add file as transcription.audio_file
        with open(t.wav_file.path, 'rb') as open_audio_file:
          t.audio_file = File(open_audio_file)
          t.save()

    ### SCRIPT

    #3. replace path of transcription.wav_file with server path
    #4. open new path and add file as transcription.audio_file
    #5. save transcription
