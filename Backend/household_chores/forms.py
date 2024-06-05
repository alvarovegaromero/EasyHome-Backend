from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from groups.models import UserGroup
from household_chores.models import SelectableTask, Task


class TaskChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.title} (Group: {obj.group.name}, Group ID: {obj.group.id})"


class SelectableTaskForm(forms.ModelForm):
    task = TaskChoiceField(queryset=Task.objects.all())

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get("task")
        assigned_user = cleaned_data.get("assigned_user")
        is_completed = cleaned_data.get("is_completed")
        if task:
            if self.instance.id:  # edit mode - exclude current task
                if (
                    SelectableTask.objects.filter(
                        task=task, date__gte=timezone.now() - timezone.timedelta(days=1)
                    )
                    .exclude(id=self.instance.id)
                    .exists()
                ):
                    raise ValidationError(
                        """The same task cannot be assigned more than once
                        in a 24 hour period, regardless of the user."""
                    )
            else:  # create mode
                if SelectableTask.objects.filter(
                    task=task, date__gte=timezone.now() - timezone.timedelta(days=1)
                ).exists():
                    raise ValidationError(
                        """The same task cannot be assigned more than once
                        in a 24 hour period, regardless of the user."""
                    )
            if assigned_user:
                if not UserGroup.is_member(assigned_user, task.group):
                    raise ValidationError("The assigned user must belong to the task's group.")
                if not is_completed:
                    raise ValidationError(
                        "If a user is assigned, the task must be marked as completed."
                    )
        if is_completed and not assigned_user:
            raise ValidationError("If a task is completed, a user must be assigned.")
        return cleaned_data

    class Meta:
        model = SelectableTask
        fields = "__all__"
