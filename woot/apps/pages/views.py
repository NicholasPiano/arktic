#woot.apps.pages.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext

#local
from apps.pages.forms import LoginForm
from apps.users.models import User
from apps.transcription.models import Transcription

#util
import numpy as np

#classes
class LoginView(View):
  def get(self, request):
    if request.user.is_authenticated():
      return HttpResponseRedirect('/start/')
    else:
      return render(request, 'pages/login.html', {})

  def post(self, request):
    form = LoginForm(request.POST)

    if form.is_valid():
      user = authenticate(email=request.POST['email'], password=request.POST['password'])
      if user is not None and user.is_active:
        login(request, user)
        return HttpResponseRedirect('/start/')
      else:
        return render(request, 'pages/login.html', {'invalid_username_or_password':True})
    else:
      return render(request, 'pages/login.html', {'bad_formatting':True})

class StartView(View):
  def get(self, request):
    user = request.user
    if user.is_authenticated():
      #get user object
      user = User.objects.get(email=user)

      #list of jobs
      active_jobs = user.jobs.filter(is_active=True)

      #total remaining transcriptions
      remaining_transcriptions = Transcription.objects.filter(is_active=True).count()
      transcriptions_done_by_user = len(np.unique([revision.transcription.pk for revision in user.revisions.all()]))

      return render(request, 'pages/start.html', {'user':user,
                                                  'active_jobs':active_jobs,
                                                  'remaining_transcriptions':remaining_transcriptions,
                                                  'transcriptions_done_by_user':transcriptions_done_by_user,})
    else:
      return HttpResponseRedirect('/login/')

def logout_view(request):
  logout(request)
  return HttpResponseRedirect('/login/')
