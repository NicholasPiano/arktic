#woot.apps.distribution.views

#django
from django.views.generic import View
from django.core.files import File
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

#local
from apps.distribution.models import Client, Project
from apps.distribution.tasks import scan_data, process_grammar
from apps.transcription.models import Grammar

#util
import os
import re

#vars

### CELERY
# For celery to work, two things have to be running:
# 1. RabbitMQ server with '$ rabbitmq-server' (no idea what it does)
# 2. Celery worker with '$ dm celeryd'

#classes
### Project list
class ProjectView(View):
  def get(self, request):
    if request.user.is_authenticated:
      #look through data directory and get new projects and grammars
      scan_data_task = scan_data.delay()

      return render(request, 'distribution/projects.html', {'scan_data_task':scan_data_task})
    else:
      return HttpResponseRedirect('/start/')

#methods
def scan_data_callback(request, task_id): #checks back periodically for completed task
  if request.user.is_authenticated:
    results = scan_data.AsyncResult(task_id)
    clients = Client.objects.all()

    if results.ready():
      return render(request, 'distribution/projects_scan_data_fragment.html', {'status':'success', 'clients':clients})
    else:
      return render(request, 'distribution/projects_scan_data_fragment.html', {'status':'loading', 'clients':clients})

def process_grammar_ajax(request, grammar_id_token):
  if request.user.is_authenticated:
    process_grammar_task = process_grammar.delay(grammar_id_token)
    grammar = Grammar.objects.get(id_token=grammar_id_token)

    return render(request, 'distribution/projects_process_grammar_ajax_fragment.html', {'status':'start','grammar':grammar,'process_grammar_task':process_grammar_task})

def process_grammar_ajax_callback(request, task_id, grammar_id_token):
  if request.user.is_authenticated:
    results = process_grammar.AsyncResult(task_id)
    grammar = Grammar.objects.get(id_token=grammar_id_token)

    status = 'loading'
    if results.ready():
        status = 'success'
    return render(request, 'distribution/projects_process_grammar_ajax_fragment.html', {'status':status,'grammar':grammar})

