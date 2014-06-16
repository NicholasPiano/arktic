#transcription.admin

#django
from django.contrib import admin

#local
from apps.transcription.models import Transcription, Revision, Archive, RelFile

# Register your models here.

#transcription
class RevisionInline(admin.TabularInline):
    model = Revision
    extra = 0

class TranscriptionAdmin(admin.ModelAdmin):
    inlines = [RevisionInline]

admin.site.register(Transcription, TranscriptionAdmin)

#revision
admin.site.register(Revision)

#archive
class RelFileInline(admin.TabularInline):
    model = RelFile
    extra = 0

class ArchiveAdmin(admin.ModelAdmin):
    inlines = [RelFileInline]

admin.site.register(Archive, ArchiveAdmin)

#relfile
admin.site.register(RelFile)
