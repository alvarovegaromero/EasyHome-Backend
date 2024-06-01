from rest_framework import serializers

from ..models import Expense


class ExpenseDetailSerializer(serializers.ModelSerializer):
    debtors = serializers.SerializerMethodField()
    paid_by = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "debtors", "paid_by", "group"]

    def get_debtors(self, obj):
        return [{"id": debtor.id, "username": debtor.username} for debtor in obj.debtors.all()]

    def get_paid_by(self, obj):
        return {"id": obj.paid_by.id, "username": obj.paid_by.username}
