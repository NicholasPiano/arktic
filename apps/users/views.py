#users.views

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

#local

class StartView(View):
    #landing page after logging in. shows basic user account (link to account page)
    #List of currently active.
    #New job button

    def get(self, request):
        #get user

        #profile details
        user = request.user
        if user.is_authenticated():
            #list of jobs
            jobs = 'None'

            return render(request, 'users/start.html', {'user':user,'jobs':jobs,})
        else:
            return HttpResponseRedirect('/login/')
