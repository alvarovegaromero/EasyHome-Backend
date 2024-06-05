from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=50)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="tasks")


class SelectableTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="selectable_tasks")
    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    is_completed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)  # can't be changed
