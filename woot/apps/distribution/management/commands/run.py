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
    self.stdout.write('scanning data directories...')
    scan_data()

    self.stdout.write('processing grammars...')
    for i, g in enumerate(Grammar.objects.all()):
      print([i+1, Grammar.objects.count()])
      g.process()

    self.stdout.write('processing transcriptions...')
    for i, t in enumerate(Transcription.objects.all()):
      print(['audio', i+1, Transcription.objects.count()])
      t.process()

    #get unique words and utterances
    for i, t in enumerate(Transcription.objects.all()):
      print(['words', i+1, Transcription.objects.count()])
      t.process_words()

    #projects
    for p in Project.objects.all():
      p.is_active = True
      p.save()
