#transcription.views

#django
from django.shortcuts import render
from django.views.generic import View

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
            user = User.objects.get(username=user)
            job = user.jobs.get(pk=job_id)
            client = job.client
            transcriptions = job.transcriptions.all()

            return render(request, main_transcription_templates[VERSION], {'transcriptions':transcriptions,
                                                                           'words':client.words.all(),})
        else:
            return HttpResponseRedirect('/login/')

#method views
def start_redirect(request):
    return HttpResponseRedirect('/start/')
