#pages.views

#django
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext

#local
from settings.dev import VERSION
from apps.pages.forms import LoginForm

#vars
login_templates = {'0.1':'pages/login/login.0.1.html',
                   '0.2':'pages/login/login.0.2.html',}

#classes
class LoginView(View):
    def get(self, request):
        return render(request, login_templates[VERSION], {})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(email=request.POST['email'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/start/') #go to employee summary page
            else:
                return render(request, login_templates[VERSION], {'invalid_username_or_password':True})
        else:
            return render(request, login_templates[VERSION], {'bad_formatting':True})
