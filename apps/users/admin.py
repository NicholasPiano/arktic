#django
from django.contrib import admin

#local
from apps.users.models import User
from apps.distribution.models import Job

class JobInline(admin.TabularInline):
    model = Job
    extra = 0

class UserAdmin(admin.ModelAdmin):
    inlines = [JobInline]

admin.site.register(User, UserAdmin)
