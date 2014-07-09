#users.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect

#local
from settings.common import NUMBER_OF_TRANSCRIPTIONS_PER_JOB
from apps.distribution.models import Client, Project
from apps.users.models import User

#class views
class StartView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated():
            #get user object
            user = User.objects.get(email=user)

            #list of jobs
            jobs = user.jobs.filter(is_active=True)

            return render(request, 'users/start.html', {'user':user,'jobs':jobs,})
        else:
            return HttpResponseRedirect('/login/')

#method views
def create_new_job(request):
    if request.method == 'GET':
        user = request.user
        if user.is_authenticated():
            #get oldest project
            project = Project.objects.all().order_by('date_created')[0]

            #get user object
            user = User.objects.get(email=user)

            #create job
            job = user.jobs.create(client=project.client, project=project, active_transcriptions=NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
            job.get_transcription_set()
            job.save()

            return HttpResponseRedirect('/transcription/' + str(job.pk))
        else:
            return HttpResponseRedirect('/login/')
