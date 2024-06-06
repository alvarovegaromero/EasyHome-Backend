from django.contrib import admin
from household_chores.forms import AssignableTaskForm
from household_chores.models import AssignableTask, Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "id", "group_name", "group_id")

    def group_name(self, obj):
        return obj.group.name

    group_name.short_description = "Group Name"


class AssignableTaskAdmin(admin.ModelAdmin):
    form = AssignableTaskForm
    list_display = (
        "task_title",
        "id",
        "group_id",
        "group_name",
        "assigned_user",
        "is_completed",
        "date",
    )

    def task_title(self, obj):
        return obj.task.title

    task_title.short_description = "Task Title"

    def group_id(self, obj):
        return obj.task.group.id

    group_id.short_description = "Group ID"

    def group_name(self, obj):
        return obj.task.group.name

    group_name.short_description = "Group Name"


admin.site.register(Task, TaskAdmin)
admin.site.register(AssignableTask, AssignableTaskAdmin)
