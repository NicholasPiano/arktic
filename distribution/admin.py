#django
from django.contrib import admin

#local
from distribution.models import Distributor, Job
from archive.models import Archive

class ArchiveInline(admin.TabularInline):
    model = Archive
    extra = 0

class DistributorAdmin(admin.ModelAdmin):
    inlines = [ArchiveInline]
    actions = ['delete_model']

    #custom action for bulk deletion
    def delete_model(self, request, obj):
        try:
            for o in obj.all():
                o.delete()
        except AttributeError:
            obj.delete()
    delete_model.short_description = 'Delete selected distributors'

    def get_actions(self, request):
        actions = super(DistributorAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def save_model(self, request, obj, form, change):
        obj.save()
        super(DistributorAdmin, self).save_model(request, obj, form, change)

admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Job)
