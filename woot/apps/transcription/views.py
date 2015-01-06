#woot.apps.transcription.views

#django
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect

#local
from apps.users.models import User
from apps.distribution.models import Project, Job
from apps.transcription.models import Transcription, Revision, Action
from libs.utils import generate_id_token

#util
import random
import json

#class views
class TranscriptionView(View):
  def get(self, request, job_id_token):
    user = request.user
    if user.is_authenticated():
      user = User.objects.get(email=user)

      job = get_object_or_404(user.jobs, id_token=job_id_token) #does this do 'return HTTP... blah'?

      #transcriptions
      transcriptions = job.transcriptions.all()
      for transcription in transcriptions:
        transcription.set_latest_revision_done_by_current_user(user)
        transcription.update()

      #words
      words = []
      if user.autocomplete_setting!='off':
        project = job.project
        if user.autocomplete_setting=='full':
          words = sorted(project.words.filter(unique=True), key=lambda word: len(word.char), reverse=False)
        else: #tags
          words = project.words.filter(unique=True, tag=True)
      words = json.dumps([word.char for word in words])

      #render
      return render(request, 'transcription/transcription.html', {'transcriptions':transcriptions,'words':words,'job_id':job.id_token,})
    else:
      return HttpResponseRedirect('/start/')

#methods
def create_new_job(request):
  if request.method == 'GET':
    user = request.user
    if user.is_authenticated():
      #get user object
      user = User.objects.get(email=user)

      #if there are available jobs
      if Job.objects.filter(is_available=True).count()>0:
        job = Job.objects.filter(is_available=True)[0]
        job.is_available = False
        user.jobs.add(job)
        job.save()
        return HttpResponseRedirect('/transcription/' + str(job.id_token))
      else:
        return HttpResponseRedirect('/start/')

    else:
      return HttpResponseRedirect('/login/')

def start_redirect(request):
  return HttpResponseRedirect('/start/')

def action_register(request):
  if request.user.is_authenticated:
    #get POST vars
    job_id = request.POST['job_id']
    transcription_id = request.POST['transcription_id']
    action_name = request.POST['action_name']
    audio_time = request.POST['audio_time']

    #get user object
    user = User.objects.get(email=request.user)

    #get transcription, client, job
    job = Job.objects.get(id_token=job_id)
    transcription = Transcription.objects.get(id_token=transcription_id)
    client = transcription.client

    #get or create revision (unique to job and user)
    revision, created = transcription.revisions.get_or_create(user=user, job=job)

    if created:
      revision.id_token = generate_id_token(Revision)
      revision.save()

    #cull
    transcription.revisions.filter(id_token=revision.id_token).exclude(pk=revision.pk).delete()

    #make action object
    revision.actions.create(client=client, job=job, user=user, transcription=transcription, id_token=generate_id_token(Action), char=action_name, audio_time=float(audio_time))

    return HttpResponse(revision.id_token)

def update_revision(request):
  if request.user.is_authenticated:
    #get POST vars
    revision_id = request.POST['revision_id']
    utterance = request.POST['utterance']
    audio_time = request.POST['audio_time']

    #get user and update revision utterance
    revision = Revision.objects.get(id_token=revision_id)

    #split utterance
    revision.utterance = utterance
    revision.audio_time = float(audio_time)
    revision.save()
    revision.process_words()
    revision.transcription.project.update()

    return HttpResponse('')

def add_word(request):
  if request.user.is_authenticated:
    #get POST vars
    transcription_id = request.POST['transcription_id']
    word = request.POST['word']

    #vars
    transcription = Transcription.objects.get(id_token=transcription_id)
    client = transcription.client
    if client.words.filter(project=transcription.project, char=word).count()==0:
      client.words.create(project=transcription.project, grammar=transcription.grammar, char=word, tag=(('[' in word or ']' in word) and ' ' not in word))

    return HttpResponse('')

'''

http://stackoverflow.com/a/2257449/2127199
http://stackoverflow.com/a/23728630/2213647

This Stack Overflow quesion is the current top Google result for "random string Python". The current top answer is:

''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

This is an excellent method, but the PRNG in random is not cryptographically secure.
I assume many people researching this question will want to generate random strings for encryption or passwords.
You can do this securely by making a small change in the above code:

''.join(random.SystemRandom().choice(string.uppercase + string.digits) for _ in xrange(n))

Using random.SystemRandom() instead of just random uses /dev/urandom on *nix machines and CryptGenRandom() in Windows.
These are cryptographically secure PRNGs. Using random.choice instead of random.SystemRandom().choice in an application
that requires a secure PRNG could be potentially devastating, and given the popularity of this question,
I bet that mistake has been made many times already.

'''
