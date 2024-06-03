from rest_framework import serializers

from ..models import Expense


class ExpensesGetSerializer(serializers.ModelSerializer):
    paid_by = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "paid_by"]

    def get_paid_by(self, obj):
        return {"id": obj.paid_by.id, "username": obj.paid_by.username}
