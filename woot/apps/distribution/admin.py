#distribution.admin

#django
from django.contrib import admin

#local
from apps.distribution.models import Client, Project, Job, Action, CompletedProject
from apps.transcription.models import Transcription, Archive

#vars

#classes
class ArchiveInline(admin.TabularInline):
    model = Archive
    extra = 0

class ProjectInline(admin.TabularInline):
    model = Project
    extra = 0

class JobInline(admin.TabularInline):
    model = Job
    extra = 0

class TranscriptionInline(admin.TabularInline):
    model = Transcription
    extra = 0

#CLIENT
class ClientAdmin(admin.ModelAdmin):
    #display all jobs and archives
    inlines = [ProjectInline, JobInline,]

admin.site.register(Client, ClientAdmin)

#PROJECT
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ArchiveInline, JobInline]

admin.site.register(Project, ProjectAdmin)
admin.site.register(CompletedProject)

#JOB
class JobAdmin(admin.ModelAdmin):
    inlines = [TranscriptionInline,]

admin.site.register(Job, JobAdmin)

#ACTION
admin.site.register(Action)
