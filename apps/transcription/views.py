#transcription.views
#meant to be used by employees doing transcription jobs

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth.models import User as DUser

#local
from apps.transcription.models import Transcription, Revision
from apps.distribution.models import Job, Client
from apps.users.models import User

#util
import string as st

#class vars


class MainJobView(View):
    #This is the main transcription interface. Transcriptions are done in batches of ~50 known as Jobs. The page is
    #essentially a giant form that is submitted whenever a certain point is reached.

    #template
    #template_name = 'main_transcription_interface.html'

    #override view methods
    def get(self, request):
        #check permission
        if request.user.is_authenticated():
            #client with least transcriptions left
            client = Client.objects.get(name='Allstate')

            #get user - a bit convoluted
            d_user = DUser.objects.get(username=request.user)
            user = User.objects.get(user=d_user)

            job = client.jobs.create(user=user)
            transcriptions = job.transcriptions.all()
            words = []
            for word in client.words.all():
                words.append(word.char) #also need to sort by length
            return render(request, 'transcription/main_transcription.html', {'transcriptions':transcriptions,
                                                                             'words':words})
        else:
            return HttpResponseRedirect('/login/')
