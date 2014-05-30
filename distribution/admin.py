#django
from django.contrib import admin

#local
from distribution.models import Distributor, Job
from archive.models import Archive

#define admin
class ArchiveInline(admin.TabularInline):
	model = Archive
	extra = 0

class DistributorAdmin(admin.ModelAdmin):
	inlines = [ArchiveInline]
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
		actions = super(DistributorAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

admin.site.register(Distributor, DistributorAdmin)
admin.site.register(Job)
