from django.contrib import admin

from .forms import ExpenseForm
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    list_display = ("name", "get_group_name", "get_group_id")

    def get_group_name(self, obj):
        return obj.group.name

    get_group_name.short_description = "Shared Board Group Name"

    def get_group_id(self, obj):
        return obj.group.id

    get_group_id.short_description = "Group ID"


admin.site.register(Expense, ExpenseAdmin)
