#users.views

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User as DjangoUser

#local
from arktic.settings import VERSION
from apps.distribution.models import Client
from apps.users.models import User

class StartView(View):
    #landing page after logging in. shows basic user account (link to account page)
    #List of currently active.
    #New job button

    def get(self, request):
        #get user

        #profile details
        user = request.user
        if user.is_authenticated():
            #get user object
            django_user = DjangoUser.objects.get(username=user)
            user = User.objects.get(user=django_user)

            #list of jobs
            jobs = user.jobs.filter(is_active=True)

            return render(request, 'users/start/'+str(VERSION)+'.html', {'user':user,'jobs':jobs,})
        else:
            return HttpResponseRedirect('/login/')

def create_new_job(request):
    #get client with most remaining trancriptions
    client = Client.objects.get() #currently just allstate

    #get user object
    django_user = DjangoUser.objects.get(username=request.user)
    user = User.objects.get(user=django_user)

    job = user.jobs.create(client=client)
    return HttpResponseRedirect('/transcription/' + str(job.pk))
