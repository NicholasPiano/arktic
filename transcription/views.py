#transcription.views

#django
from django.shortcuts import render
from django.http import HttpResponse

#local
from transcription.models import Transcription

transcription_index = 0

# Create your views here.
def index(request):
    t = Transcription.objects.all()[transcription_index]
    return render(request, 'transcription/main_transcription.html', {
        'transcription':t ,
    })
