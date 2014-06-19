#transcription.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

#local
from settings.dev import VERSION
from apps.users.models import User

#vars
main_transcription_templates = {'0.1':'transcription/main_transcription/main_transcription.0.1.html',
                                '0.2':'transcription/main_transcription/main_transcription.0.2.html',}

#class views
class MainTranscriptionView(View):
    def get(self, request, job_id):
        user = request.user
        if user.is_authenticated():
            user = User.objects.get(email=user)

            #get job
            job = get_object_or_404(user.jobs, pk=job_id) #In truth, I should

            client = job.client
            transcriptions = job.transcriptions.all()
            words = client.words.all()

            return render(request, main_transcription_templates[VERSION], {'transcriptions':transcriptions,
                                                                           'words':words,
                                                                           'job_id':job_id,})
        else:
            return HttpResponseRedirect('/login/')

#method views
def start_redirect(request):
    return HttpResponseRedirect('/start/')
