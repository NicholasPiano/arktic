#transcription.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404

#local
from apps.users.models import User

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
            for transcription in transcriptions:
                transcription.latest_revision_words(user)
                transcription.save()
            words = sorted(client.words.all(), key=lambda x: len(x.content), reverse=False)

            #remaining transcriptions in project
            project = job.project
            remaining_transcriptions = project.transcriptions.filter(is_active=True).count()

            return render(request, 'transcription/transcription.html', {'transcriptions':transcriptions,
                                                                        'words':words,
                                                                        'job_id':job_id,
                                                                        'remaining_transcriptions':remaining_transcriptions,})
        else:
            return HttpResponseRedirect('/login/')

#method views
def start_redirect(request):
    return HttpResponseRedirect('/start/')
