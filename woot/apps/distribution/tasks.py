#apps.distribution.tasks

#django
from django.conf import settings

#local
from apps.distribution.models import Client, Project
from apps.transcription.models import Grammar
from apps.transcription.models import Transcription, CSVFile, WavFile
from libs.utils import generate_id_token

#util
import os

#third party
from celery import task

#from apps.distribution.tasks import scan_data; scan_data();

@task()
def scan_data():
  '''
  Walks through data directory and finds new grammars, creating them and adding them to the right clients and projects.
  '''

  #1. get all filenames+paths in project dir
  #2. get all filenames from all csv files in project dir -> dictionary
  #3.

  data_dir = os.path.join(settings.DJANGO_ROOT, 'data')
  for name in os.listdir(data_dir):
    client, created = Client.objects.get_or_create(name=name)

    if created: #scan directory for grammars
      client.client_path = os.path.join(data_dir, name)
      client.save()
      print('created client: ' + str(client))

    for project_name in [dir_i for dir_i in os.listdir(client.client_path) if os.path.isdir(os.path.join(client.client_path, dir_i))]:
      project, created = client.projects.get_or_create(name=project_name)

      if created:
        project.id_token = generate_id_token(Project)
        project.project_path = os.path.join(client.client_path, project_name)
        project.save()
        print('created project: ' + str(project))

      #generate list of .csv files and list of .wav files
      csv_file_list = []
      wav_file_dictionary = {}
      for sup, subs, file_list in os.walk(project.project_path):
        for file_name in file_list:
          if '.csv' in file_name and 'Unsorted' not in sup and 'save' not in sup:
            csv_file_list.append(file_name)
            root, ext = os.path.splitext(file_name)
            project.csv_files.get_or_create(client=client, name=root, file_name=file_name, path=sup)
          elif '.wav' in file_name:
            wav_file_dictionary[file_name] = os.path.join(sup, file_name)

      for i, csv_file in enumerate(project.csv_files.all()):
        grammar, created = project.grammars.get_or_create(client=client, name=csv_file.name)

        if created:
          grammar.csv_file = csv_file
          grammar.id_token = generate_id_token(Grammar)
          print('created grammar ' + str(grammar))

          with open(os.path.join(csv_file.path, csv_file.file_name)) as open_rel_file:
            lines = open_rel_file.readlines()
            for j, line in enumerate(lines):
              tokens = line.split('|') #this can be part of a relfile parser object with delimeter '|'
              transcription_audio_file_name = os.path.basename(tokens[0])
              grammar.wav_files.get_or_create(client=client, project=project, path=wav_file_dictionary[transcription_audio_file_name], file_name=transcription_audio_file_name)
              print('grammar %d/%d, wav %d/%d'%(i+1,project.csv_files.count(),j+1,len(lines)), end='\r' if j<len(lines)-1 else '\n')

          grammar.save()
          csv_file.save()

@task()
def process_grammar(grammar_id_token):
  grammar = Grammar.objects.get(id_token=grammar_id_token)
  grammar.process()
  for transcription in grammar.transcriptions.all():
    transcription.process()
