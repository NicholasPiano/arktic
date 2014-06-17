#distribution.admin

#django
from django.contrib import admin

#local
from apps.distribution.models import Client, Job, Action
from apps.transcription.models import Transcription, Archive

#vars

#classes
#CLIENT
class ArchiveInline(admin.TabularInline):
    model = Archive
    extra = 0

class JobInline(admin.TabularInline):
    model = Job
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    #display all jobs and archives
    inlines = [ArchiveInline, JobInline,]

admin.site.register(Client, ClientAdmin)

#JOB
class TranscriptionInline(admin.TabularInline):
    model = Transcription
    extra = 0

class JobAdmin(admin.ModelAdmin):
    inlines = [TranscriptionInline,]

admin.site.register(Job, JobAdmin)

#ACTION
admin.site.register(Action)
