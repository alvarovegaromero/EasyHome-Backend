from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    paid_by_username = serializers.CharField(source="paid_by.username", read_only=True)

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "paid_by_username"]
