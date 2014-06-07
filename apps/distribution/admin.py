#django
from django.contrib import admin

#local
from apps.distribution.models import Client, Job
from apps.transcription.models import Archive, Transcription

# Register your models here.
#job

class TranscriptionInline(admin.TabularInline):
    model = Transcription
    extra = 0

class JobAdmin(admin.ModelAdmin):
    inlines = [TranscriptionInline]
    actions = ['delete_model', 'get_transcription_set']

    #custom action for bulk deletion
    def delete_model(self, request, obj):
        try:
            for o in obj.all():
                o.delete()
        except AttributeError:
            obj.delete()
    delete_model.short_description = 'Delete selected Jobs'

    #generate list of transcriptions
    def get_transcription_set(self, request, obj):
        try:
            for o in obj.all():
                o.get_transcription_set()
        except AttributeError:
            obj.get_transcription_set()

    def get_actions(self, request):
        actions = super(JobAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.save()
        super(JobAdmin, self).save_model(request, obj, form, change)

admin.site.register(Job, JobAdmin)

#client
class ArchiveInline(admin.TabularInline):
    model = Archive
    extra = 0

class ClientAdmin(admin.ModelAdmin):
    inlines = [ArchiveInline]
    actions = ['delete_model']

    #custom action for bulk deletion
    def delete_model(self, request, obj):
        try:
            for o in obj.all():
                o.delete()
        except AttributeError:
            obj.delete()
    delete_model.short_description = 'Delete selected clients'

    def get_actions(self, request):
        actions = super(ClientAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.save()
        super(ClientAdmin, self).save_model(request, obj, form, change)

admin.site.register(Client, ClientAdmin)
