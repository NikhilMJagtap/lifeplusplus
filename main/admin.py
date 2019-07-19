from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as  BaseUserAdmin
from django.contrib.auth.models import User
from main.models import Profile, Req

# Register your models here.

class ProfileInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profiles'

class UserAdmin(BaseUserAdmin):
    inlines=(ProfileInLine,)


admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(Req)