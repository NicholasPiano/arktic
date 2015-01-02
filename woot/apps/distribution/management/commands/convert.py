#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.transcription.models import WavFile
from subprocess import call

#util
import json

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #run each shell command on all audio files
    for wavefile in WavFile.objects.all():
      cmd = ['ffmpeg','-y','-i',wavefile.path,'-f','wav',wavefile.path]
      call(cmd)
