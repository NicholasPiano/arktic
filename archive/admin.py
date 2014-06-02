#archive.admin

#django
from django.contrib import admin

#local
from archive.models import Archive, RelFile

# Register your models here.
class RelFileInline(admin.TabularInline):
	model = RelFile

class ArchiveAdmin(admin.ModelAdmin):
    inlines = [RelFileInline]
    actions = ['delete_model']

    def delete_model(self, request, object):
        try:
            for obj in object.all():
                obj.delete()
        except AttributeError:
            object.delete()
    delete_model.short_description = 'Delete selected archives'

    def get_actions(self, request):
        actions = super(ArchiveAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

admin.site.register(Archive, ArchiveAdmin)
admin.site.register(RelFile)
