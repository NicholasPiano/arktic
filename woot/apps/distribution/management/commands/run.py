#django
from django.core.management.base import BaseCommand, CommandError

#local
from apps.transcription.models import Grammar, Transcription, Word
from apps.distribution.tasks import scan_data

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
#     scan_data()
    for g in Grammar.objects.all():
#       g.process()
      for t in g.transcriptions.all():
        t.process()
#     for w in Word.objects.all():
#       print(w)
