#django
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

#local
from apps.transcription.models import Grammar, Transcription, Word
from apps.distribution.models import Project
from apps.distribution.tasks import scan_data

#util
import json
import shutil as sh
import os

#command
class Command(BaseCommand):
  args = '<none>'
  help = ''

  def handle(self, *args, **options):
    root_path = os.path.dirname(settings.MEDIA_ROOT)
    path = os.path.join(settings.MEDIA_ROOT, 'upload')

    p = Project.objects.get(client__name='allstate')

    count = p.transcriptions.count()
    for i,t in enumerate(p.transcriptions.all()):
      print([i, count, t.audio_file.url])
      sh.copy2(os.path.join(root_path, str(t.audio_file.url).strip('/')), path)
