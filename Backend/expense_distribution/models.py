from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    name = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    group = models.OneToOneField("groups.Group", on_delete=models.CASCADE)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="paid_expenses")
    debtors = models.ManyToManyField(User, related_name="debtors")
    date_added = models.DateTimeField(auto_now_add=True)  # can't be changed
    date_paid = models.DateTimeField(default=timezone.now)  # can be changed in the future
