from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from groups.models import UserGroup


class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    group = models.ForeignKey("groups.Group", on_delete=models.CASCADE, related_name="expenses")
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")
    debtors = models.ManyToManyField(User, related_name="debtors")
    date_added = models.DateTimeField(auto_now_add=True)  # can't be changed
    date_paid = models.DateTimeField(default=timezone.now)  # can be changed in the future

    def clean(self):
        # Check if paid_by user is in the same group
        if not UserGroup.objects.filter(user=self.paid_by, group=self.group).exists():
            raise ValidationError("The user who paid must be in the same group.")

        # Check if all debtors are in the same group
        for debtor in self.debtors.all():
            if not UserGroup.objects.filter(user=debtor, group=self.group).exists():
                raise ValidationError("All debtors must be in the same group.")
