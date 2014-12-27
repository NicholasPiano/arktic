#woot.apps.distribution.views

#django
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

#local
from apps.distribution.models import Client, Project

#vars

#classes
### Project list
class ProjectView(View):
  def get(self, request):
    if request.user.is_authenticated:

      #look through data directory and get new projects and grammars
      scan_data()

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
