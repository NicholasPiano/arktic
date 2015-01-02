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
    self.stdout.write('processing grammars...')
    for i, g in enumerate(Grammar.objects.all()):
      print([i+1, Grammar.objects.count()])
      g.process()
