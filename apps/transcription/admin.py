#django
from django.contrib import admin

#local
from apps.transcription.models import Transcription

# Register your models here.
admin.site.register(Transcription)
