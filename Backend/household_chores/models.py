from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_default_date():
    return timezone.now().date()


class Task(models.Model):
    title = models.CharField(max_length=50)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="tasks")


class AssignableTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="selectable_tasks")
    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tasks"
    )
    is_completed = models.BooleanField(default=False)
    date = models.DateField(default=get_default_date)
