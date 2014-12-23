#woot.apps.transcription.views

#django

#local

#class views
class MainTranscriptionView(View):
  def get(self, request, job_id):

#method views
def start_redirect(request):
  return HttpResponseRedirect('/start/')
