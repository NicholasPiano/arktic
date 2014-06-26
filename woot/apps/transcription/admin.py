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
class ArchiveAdmin(admin.ModelAdmin):
    change_form_template = 'progressbarupload/change_form.html'
    add_form_template = 'progressbarupload/change_form.html'

admin.site.register(Archive, ArchiveAdmin)

#RELFILE
admin.site.register(RelFile)
