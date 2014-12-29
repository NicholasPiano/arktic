#woot.apps.distribution.views

#django
from django.views.generic import View
from django.core.files import File
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

#local
from apps.distribution.models import Client, Project, Grammar
from apps.transcription.models import Transcription
from libs.utils import generate_id_token

#util
import os
import re
from datetime import datetime as dt

#vars

#classes
### Project list
class ProjectView(View):
  def get(self, request):
    if request.user.is_authenticated:

      #look through data directory and get new projects and grammars
      data_dir = os.path.join(settings.DJANGO_ROOT, 'data')
      for name in os.listdir(data_dir):
        client, created = Client.objects.get_or_create(name=name)

        if created: #scan directory for grammars
          client.client_path = os.path.join(data_dir, name)
          client.save()

        for project_name in os.listdir(client.client_path):
          project, created = client.projects.get_or_create(name=project_name)

          if created:
            project.id_token = generate_id_token(Project)
            project.project_path = os.path.join(client.client_path, project_name)
            project.save()

          #generate list of .csv files and list of .wav files
          csv_file_list = []
          wav_file_dictionary = {}
          for sup, subs, file_list in os.walk(project.project_path):
            for file_name in file_list:
              if '.csv' in file_name:
                csv_file_list.append(os.path.join(sup, file_name))
              elif '.wav' in file_name:
                wav_file_dictionary[file_name] = os.path.join(sup, file_name)

          for i, complete_grammar_path in enumerate(csv_file_list):
            complete_grammar_name = os.path.basename(complete_grammar_path)
            root, ext = os.path.splitext(complete_grammar_name)
            grammar, created = project.grammars.get_or_create(client=client, name=root)

            if created:
              grammar.id_token = generate_id_token(Grammar)
              grammar.client = client
              grammar.grammar_path = complete_grammar_name
              grammar.save()
#               with open(complete_grammar_path) as open_relfile:
#                 lines = open_relfile.readlines()
#                 for j, line in enumerate(lines):
#                   tokens = line.split('|') #this can be part of a relfile parser object with delimeter '|'
#                   transcription_audio_file_name = os.path.basename(tokens[0]).rstrip()
#                   confidence = tokens[2]
#                   utterance = tokens[3].strip() if ''.join(tokens[3].split()) != '' else ''
#                   value = tokens[4]
#                   confidence_value = tokens[5].rstrip() #chomp newline
#                   if confidence_value is not '':
#                       confidence_value = float(float(confidence_value)/1000.0) #show as decimal
#                   else:
#                       confidence_value = 0.0

#                   if transcription_audio_file_name in wav_file_dictionary:
#                     print([dt.now(),('grammar %d/%d '%(i,len(csv_file_list))) + ('transcription %d/%d'%(j,len(lines)))])
#                     with open(wav_file_dictionary[transcription_audio_file_name], 'rb') as open_audio_file:
#                       grammar.transcriptions.create(client=grammar.client,
#                                                     project=grammar.project,
#                                                     id_token=generate_id_token(Transcription),
#                                                     audio_file=File(open_audio_file),
#                                                     grammar=grammar,
#                                                     confidence=confidence,
#                                                     utterance=utterance,
#                                                     value=value,
#                                                     confidence_value=confidence_value)

      clients = Client.objects.all()
      return render(request, 'distribution/projects.html', {'clients':clients})
    else:
      return HttpResponseRedirect('/start/')

### PLAN

# Stage 1:
## 1. A view that can load a list of projects having scanned the 'data' directory
#### a) also load existing projects
## 2. displays a list of clients with projects under them.

# Stage 2:
## 1. If loading the project list is too hard, make a separate task and let that run.
## 2. Make a callback for each project
