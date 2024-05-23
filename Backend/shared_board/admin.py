from django.contrib import admin
from .models import SharedBoard

# Register your models here.


class SharedBoardAdmin(admin.ModelAdmin):
    list_display = ("get_group_name", "get_group_id")
    readonly_fields = ("group",)  # group can not be changed

    def has_add_permission(self, request):
        return False

    def get_group_name(self, obj):
        return obj.group.name

    get_group_name.short_description = "Shared Board Group Name"

    def get_group_id(self, obj):
        return obj.group.id

    get_group_id.short_description = "Group ID"


admin.site.register(SharedBoard, SharedBoardAdmin)
