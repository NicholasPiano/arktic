#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.transcription.models import Grammar, Transcription, Word
from apps.distribution.models import Project
from apps.distribution.tasks import scan_data

#util
import json

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    #get unique words and utterances
    for i, t in enumerate(Transcription.objects.all()):
      print(['words', i+1, Transcription.objects.count()])
      t.process_words()
