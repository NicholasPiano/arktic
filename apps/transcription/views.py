#transcription.views
#meant to be used by employees doing transcription jobs

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

#local
from apps.transcription.models import Transcription, Revision
from apps.distribution.models import Job

#util

#class vars


class MainJobView(View):
    #This is the main transcription interface. Transcriptions are done in batches of ~50 known as Jobs. The page is
    #essentially a giant form that is submitted whenever a certain point is reached.

    #template
    #template_name = 'main_transcription_interface.html'

    #override view methods
    def get(self, request):
        #check permission
        #request['USER']
        #job id
        return render(request, 'transcription/main_transcription.html', {})

