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
            for word in transcription_utterance.split():
                revision.words.create(content=word)
            revision.save()

            #create new action object to mark the completion of another revision
            button_id = 'closing revision: #' + str(revision.pk)
            action = job.actions.create(user=job.user, button_id=button_id, transcription_id=transcription_id)
            action.save()

    except Revision.DoesNotExist:
        revision = transcription.revisions.create(user=job.user, utterance=transcription_utterance)
        for word in transcription_utterance.split():
            revision.words.create(content=word)
        revision.save()

        #create new action object to mark the completion of another revision
        button_id = 'closing revision: #' + str(revision.pk)
        action = job.actions.create(user=job.user, button_id=button_id, transcription_id=transcription_id)
        action.save()

    transcription.update()
    transcription.save()

    #check archive and compress
    relfile = transcription.relfile
    relfile.update()
    relfile.save()
    #transcription.relfile.archive.check_transcriptions()

    #check job and calculate remaining transcriptions
    job.update()
    job.save()

    #save project
    project = job.project
    project.update()
    project.save()

    #client for export
    client = project.client
    client.update()
    client.save()

    #return status
    return json.dumps({'status':'success'})
