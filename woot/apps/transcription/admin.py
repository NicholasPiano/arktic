#transcription.admin

#django
from django.contrib import admin

#local
from apps.transcription.models import Transcription, Revision, Archive, RelFile

#vars

#classes
#TRANSCRIPTION
admin.site.register(Transcription)

#REVISION
admin.site.register(Revision)

#ARCHIVE
admin.site.register(Archive)

#RELFILE
admin.site.register(RelFile)
