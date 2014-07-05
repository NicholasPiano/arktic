#pages.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext

#local
from apps.pages.forms import LoginForm

#classes
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/start/')
        else:
            return render(request, 'pages/login.html', {})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/start/') #go to employee summary page
            else:
                return render(request, 'pages/login.html', {'invalid_username_or_password':True})
        else:
            return render(request, 'pages/login.html', {'bad_formatting':True})
