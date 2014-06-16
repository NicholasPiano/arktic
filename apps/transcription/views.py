#transcription.views
#meant to be used by employees doing transcription jobs

#django
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

#local
from arktic.settings import VERSION
from apps.distribution.models import Job, Client

#util
import string as st

#class vars


class MainJobView(View):
    #This is the main transcription interface. Transcriptions are done in batches of ~50 known as Jobs.

    #override view methods
    def get(self, request, job_id):
        #check permission
        if request.user.is_authenticated():
            #client with least transcriptions left
            client = Client.objects.get(name='Allstate')

            job = get_object_or_404(Job, pk=job_id)
            transcriptions = job.transcriptions.all()
            words = []
            for word in client.words.all():
                words.append(word.char) #also need to sort by length
            return render(request, 'transcription/main_transcription/'+ str(VERSION) +'.html', {'transcriptions':transcriptions,
                                                                                                'words':words})
        else:
            return HttpResponseRedirect('/login/')
