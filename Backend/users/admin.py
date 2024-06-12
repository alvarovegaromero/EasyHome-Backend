from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User


class UserAdmin(DefaultUserAdmin):
    list_display = ("username", "id", "email", "first_name", "last_name", "last_login")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
