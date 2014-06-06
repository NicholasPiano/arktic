#pages.views

#django
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import View

#local

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
    #home page

    #template

    #override view methods
    def get(self, request):


        return HttpResponse('login')
