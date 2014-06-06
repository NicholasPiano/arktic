#django
from django.contrib import admin

#local
from apps.transcription.models import Transcription, Revision, Archive, RelFile

# Register your models here.
admin.site.register(Transcription)
admin.site.register(Revision)
admin.site.register(Archive)
admin.site.register(RelFile)
