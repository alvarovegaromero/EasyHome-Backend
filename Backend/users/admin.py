from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import User
from users.models import UserProfile


class UserAdmin(DefaultUserAdmin):
    list_display = ("username", "id", "email", "first_name", "last_name", "last_login")


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "user_id", "reset_password_token", "has_email_verified", "last_login")

    def user_id(self, obj):
        return obj.user.id

    user_id.short_description = "User ID"

    def last_login(self, obj):
        return obj.user.last_login

    last_login.short_description = "Last Login"


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
