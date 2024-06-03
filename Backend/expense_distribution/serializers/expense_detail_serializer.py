from rest_framework import serializers

from ..models import Expense


class ExpenseDetailSerializer(serializers.ModelSerializer):
    debtors = serializers.SerializerMethodField()
    paid_by = serializers.SerializerMethodField()
    date_paid = serializers.SerializerMethodField()
    date_added = serializers.SerializerMethodField()

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "debtors", "paid_by", "group", "date_added"]

    def get_debtors(self, obj):
        return [{"id": debtor.id, "username": debtor.username} for debtor in obj.debtors.all()]

    def get_paid_by(self, obj):
        return {"id": obj.paid_by.id, "username": obj.paid_by.username}

    def get_date_paid(self, obj):
        return obj.date_paid.strftime("%Y-%m-%d")

    def get_date_added(self, obj):
        return obj.date_added.strftime("%Y-%m-%d")
