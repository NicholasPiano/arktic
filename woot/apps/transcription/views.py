#woot.apps.transcription.views

#django
from django.views.generic import View
from django.conf import settings
from django.shortcuts import get_object_or_404

#local
from apps.users.models import User
from apps.distribution.models import Project, Job

#util
import random

#class views
class TranscriptionView(View):
  def get(self, request, job_id_token):
    user = request.user
    if user.is_authenticated():
      user = User.objects.get(email=user)

      job = get_object_or_404(user.jobs, id_token=job_id_token)

      #transcriptions
      transcriptions = job.transcriptions.all()

      #words
      words = []
      if user.autocomplete_setting!='off':
        project = job.project
        if user.autocomplete_setting=='full':
          words = sorted(project.words.filter(unique=True), key=lambda word: len(word.char), reverse=False)
        else: #tags
          words = project.words.filter(unique=True, tag=True)

      #render
      return render(request, 'transcription/transcription.html', {'transcriptions':transcriptions,'words':words})
    else:
      return HttpResponseRedirect('/start/')

#methods
def id_generator(size=settings.JOB_ID_LENGTH, chars=settings.JOB_ID_CHARS):
  return ''.join(random.choice(chars) for _ in range(size))

def create_new_job(request):
  if request.method == 'GET':
    user = request.user
    if user.is_authenticated():
      #get oldest active project
      project = Project.objects.filter(is_active=True).order_by('date_created')[0]

      #get user object
      user = User.objects.get(email=user)

      #create job
      id_token = id_generator()
      id_tokens = [job.id_token for job in Job.objects.all()]
      while id_token in id_tokens: #check that id_token does not already exist
        id_token = id_generator()

      job = user.jobs.create(client=project.client, project=project, id_token=id_token, active_transcriptions=settings.NUMBER_OF_TRANSCRIPTIONS_PER_JOB)
      job.get_transcription_set()

      return HttpResponseRedirect('/transcription/' + str(job.id_token))
    else:
      return HttpResponseRedirect('/login/')

def start_redirect(request):
  return HttpResponseRedirect('/start/')

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
