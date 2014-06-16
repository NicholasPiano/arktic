#user.admin

#django
from django.contrib import admin

#local
from apps.users.models import User
from apps.distribution.models import Job
from apps.transcription.models import Revision

#user
class JobInline(admin.TabularInline):
    model = Job
    extra = 0

class RevisionInline(admin.TabularInline):
    model = Revision
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [JobInline, RevisionInline]

admin.site.register(User, UserAdmin)
