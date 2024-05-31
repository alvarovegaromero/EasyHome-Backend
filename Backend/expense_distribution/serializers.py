from django.contrib.auth.models import User
from groups.models import Group, UserGroup
from rest_framework import serializers

from .models import Expense


class ExpenseGetSerializer(serializers.ModelSerializer):
    paid_by_username = serializers.CharField(source="paid_by.username", read_only=True)

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "paid_by_username"]


class ExpensePostSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    amount = serializers.DecimalField(max_digits=7, decimal_places=2)
    debtors = serializers.ListField(child=serializers.IntegerField())
    paid_by = serializers.IntegerField()
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    date_paid = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"], required=False)

    class Meta:
        model = Expense
        fields = ["id", "name", "amount", "date_paid", "debtors", "paid_by", "group"]

    def validate(self, data):
        """
        Check data is valid before creating the object
        """
        name = data.get("name")
        amount = data.get("amount")
        debtors = data.get("debtors")
        paid_by = data.get("paid_by")
        group = data.get("group")

        if not name or not amount:
            raise serializers.ValidationError("Name and amount must be provided")

        if not debtors or paid_by is None:
            raise serializers.ValidationError("Debtors and paid_by must be provided")

        if not UserGroup.is_member_by_id(user_id=paid_by, group=group):
            raise serializers.ValidationError("Payer must be a member of the group")

        for debtor_id in debtors:
            if not UserGroup.is_member_by_id(user_id=debtor_id, group=group):
                raise serializers.ValidationError("All debtors must be members of the group")

        return data

    def create(self, validated_data):
        name = validated_data.get("name")
        amount = validated_data.get("amount")
        debtors = validated_data.get("debtors")
        paid_by = validated_data.get("paid_by")
        group = validated_data.get("group")
        date_paid = validated_data.get("date_paid")

        expense = Expense.objects.create(
            name=name,
            amount=amount,
            paid_by=User.objects.get(id=paid_by),
            group=group,
            **({"date_paid": date_paid} if date_paid is not None else {})
        )

        for debtor_id in debtors:
            debtor = User.objects.get(id=debtor_id)
            expense.debtors.add(debtor)

        expense.save()

        return expense
