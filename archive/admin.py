#django
from django.contrib import admin

#local
from archive.models import Archive, RelFile

# Register your models here.
class RelFileInline(admin.TabularInline):
	model = RelFile
	extra = 0

class ArchiveAdmin(admin.ModelAdmin):
	inlines = [RelFileInline]
	actions = ['delete_model'] #add custom method

	#custom action for bulk deletion
	def delete_model(self, request, obj):
		try:
			for o in obj.all():
				o.delete()
		except AttributeError: #if only one object is selected
			obj.delete()
	delete_model.short_description = "Delete selected archives"

	#override to remove default 'delete_selected' action from list of actions
	def get_actions(self, request):
		actions = super(ArchiveAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

admin.site.register(Archive, ArchiveAdmin)
admin.site.register(RelFile)
