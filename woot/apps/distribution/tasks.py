#apps.distribution.tasks

#django
from django.conf import settings

#local
from apps.distribution.models import Client, Project, Grammar
from apps.transcription.models import Transcription
from libs.utils import generate_id_token

#util
import os

#third party
from celery import task

@task()
def scan_data():
  '''
  Walks through data directory and finds new grammars, creating them and adding them to the right clients and projects.
  '''

  data_dir = os.path.join(settings.DJANGO_ROOT, 'data')
  with open(os.path.join(data_dir, 'test.txt'), 'w') as f:
    f.write('test')

#   for name in os.listdir(data_dir):
#     client, created = Client.objects.get_or_create(name=name)

#     if created: #scan directory for grammars
#       client.client_path = os.path.join(data_dir, name)
#       client.save()

#     for project_name in os.listdir(client.client_path):
#       project, created = client.projects.get_or_create(name=project_name)

#       if created:
#         project.id_token = generate_id_token(Project)
#         project.project_path = os.path.join(client.client_path, project_name)
#         project.save()

#       #generate list of .csv files and list of .wav files
#       csv_file_list = []
#       wav_file_dictionary = {}
#       for sup, subs, file_list in os.walk(project.project_path):
#         for file_name in file_list:
#           if '.csv' in file_name:
#             csv_file_list.append(os.path.join(sup, file_name))
#           elif '.wav' in file_name:
#             wav_file_dictionary[file_name] = os.path.join(sup, file_name)

#       for i, complete_grammar_path in enumerate(csv_file_list):
#         print(i)
#         complete_grammar_name = os.path.basename(complete_grammar_path)
#         root, ext = os.path.splitext(complete_grammar_name)
#         grammar, created = project.grammars.get_or_create(client=client, name=root)

#         if created:
#           grammar.id_token = generate_id_token(Grammar)
#           grammar.client = client
#           grammar.grammar_path = complete_grammar_path
#           grammar.save()
