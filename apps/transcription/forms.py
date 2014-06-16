#transcription.forms

#django
from django import forms

#local
from apps.distribution.models import Job

class MainJobForm(forms.Form): #invisible form included with transcription interface to gather utterance data, validate it, and make revisions.

    #init
    def __init__(self, *args, **kwargs):
        job = kwargs.pop('job')
        transcription_pk_list = []
        for transcription in job.transcriptions.all():
            transcription_pk_list.append(str(transcription.pk))
        super(MainJobForm, self).__init__(*args, **kwargs)

        for pk in transcription_pk_list:
            self.fields['%s' % pk] = forms.CharField(max_length=100)
