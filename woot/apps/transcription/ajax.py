#transcription.ajax

#django

#local
from apps.distribution.models import Job, Action
from apps.transcription.models import Transcription, Revision

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
    action.save()

    #return status
    return json.dumps({'status':'success'})

@dajaxice_register
def update_transcription(request, job_id, transcription_id, transcription_utterance):
    #strip spaces
    transcription_utterance = ' '.join(transcription_utterance.split())
    #get transcription from id
    job = Job.objects.get(pk=job_id)
    transcription = Transcription.objects.get(pk=transcription_id)

    #create new revision object and add to transcription
    try:
        latest_revision = transcription.revisions.latest()
        if transcription_utterance != latest_revision.utterance:
            revision = transcription.revisions.create(user=job.user, utterance=transcription_utterance)
            revision.save()
    except Revision.DoesNotExist:
        revision = transcription.revisions.create(user=job.user, utterance=transcription_utterance)
        revision.save()

    transcription.is_active = False
    transcription.save()

    #check archive and compress
    transcription.relfile.archive.check_transcriptions()

    #check job and calculate remaining transcriptions
    job.check_transcriptions()

    #return status
    return json.dumps({'status':'success'})
