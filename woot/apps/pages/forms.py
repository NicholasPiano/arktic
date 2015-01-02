#woot.apps.pages.forms

#django
from django import forms

#classes
class LoginForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)
