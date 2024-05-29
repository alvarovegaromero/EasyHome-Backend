from django.contrib import admin

from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("name", "get_group_name", "get_group_id")

    def get_group_name(self, obj):
        return obj.group.name

    get_group_name.short_description = "Shared Board Group Name"

    def get_group_id(self, obj):
        return obj.group.id

    get_group_id.short_description = "Group ID"


admin.site.register(Expense, ExpenseAdmin)

# try to choose only among group members once the group is selected
