from django.contrib import admin

from .models import Group, UserGroup


class GroupAdmin(admin.ModelAdmin):
    list_display = ("__str__", "id", "get_owner_name")
    readonly_fields = ("join_code", "join_code_expiration")

    def get_owner_name(self, obj):
        return obj.owner.username

    get_owner_name.short_description = "Owner Name"


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ("__str__", "user_id", "group_id")


admin.site.register(Group, GroupAdmin)
admin.site.register(UserGroup, UserGroupAdmin)
