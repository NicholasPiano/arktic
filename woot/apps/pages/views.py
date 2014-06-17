#pages.views

#django
from django.shortcuts import render
from django.views.generic import View

#local
from settings.dev import VERSION

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
            user = authenticate(username=request.POST['username'], password=request.POST['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/start/') #go to employee summary page
            else:
                return render(request, login_templates[VERSION], {'invalid_username_or_password':True})
        else:
            return render(request, login_templates[VERSION], {'bad_formatting':True})
