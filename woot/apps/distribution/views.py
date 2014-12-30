#woot.apps.distribution.views

#django
from django.views.generic import View
from django.core.files import File
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

#local
from apps.distribution.models import Client
from apps.distribution.tasks import scan_data

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

      clients = Client.objects.all()
      return render(request, 'distribution/projects.html', {'clients':clients, 'scan_data_task':scan_data_task})
    else:
      return HttpResponseRedirect('/start/')

def scan_data_callback(request, task_id): #checks back periodically for completed task
  if request.user.is_authenticated:
    results = scan_data.AsyncResult(task_id)
    if results.ready():
      return HttpResponse(' Done.')
    else:
      return HttpResponse('.')
