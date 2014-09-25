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
            for job in jobs:
                if job.transcriptions.all() == []:
                    job.delete()

            jobs = user.jobs.filter(is_active=True)

            #total remaining transcriptions
            remaining_transcriptions = 0
            for project in Project.objects.filter(is_active=True):
              remaining_transcriptions += project.transcriptions.filter(is_active=True).count()

            return render(request, 'users/start.html', {'user':user,'jobs':jobs,'remaining_transcriptions':remaining_transcriptions,})
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
