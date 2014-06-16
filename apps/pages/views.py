#pages.views

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout

#local
from apps.pages.forms import LoginForm

#using expo
class IndexView(View):
    #home page

    #template

    #override view methods
    def get(self, request):
        context = {'GA_CODE':'5A'}
        return render(request, 'base.html', context)

class AboutView(View):
    #home page

    #template

    #override view methods
    def get(self, request):


        return HttpResponse('about')

class SystemView(View):
    #home page

    #template

    #override view methods
    def get(self, request):


        return HttpResponse('system')

class PricesView(View):
    #home page

    #template

    #override view methods
    def get(self, request):


        return HttpResponse('prices')

class SecurityView(View):
    #home page

    #template

    #override view methods
    def get(self, request):


        return HttpResponse('security')

class LoginView(View):

    #override view methods
    def get(self, request):
        return render(request, 'pages/login.html', {})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/start/') #go to employee summary page
            else:
                return render(request, 'pages/login.html', {'invalid_username_or_password':True})
        else:
            return render(request, 'pages/login.html', {'bad_formatting':True})
