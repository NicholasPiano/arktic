#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.transcription.models import Grammar, Transcription, Word
from apps.distribution.models import Project

#util
import json

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
#     self.stdout.write('processing transcriptions...')
#     for i, t in enumerate(Transcription.objects.all()):
#       print(['audio', i+1, Transcription.objects.count()])
    t = Transcription.objects.get(pk=1000)
    path_server = '/home/arkaeologic/arktic/woot/data/'
    path_down = '/Users/nicholaspiano/code/arktic/woot/data'
