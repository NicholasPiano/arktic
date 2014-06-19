#transcription.ajax

#django

#local
from apps.distribution.models import Job, Action

#third party
from dajaxice.decorators import dajaxice_register

#util
import json

#methods
@dajaxice_register
def action_register(request, job_id, button_id, transcription_id):
    #get name of button pressed, time info, current transcription id, current transcription utterance, etc.
    job = Job.objects.get(pk=job_id)
    action = job.actions.create(user=job.user, button_id=button_id, transcription_id=transcription_id)

    #return status
    return json.dumps({'status':'success'})

@dajaxice_register
def update_transcription(request):
    #get transcription from id
    #update utterance
    #create new revision object and add to transcription
    #return status
    return json.dumps({'status':'success'})
