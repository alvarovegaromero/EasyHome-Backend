from household_chores.models import AssignableTask
from rest_framework import serializers


class AssignableTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignableTask
        fields = ["id", "task", "assigned_user", "is_completed", "date"]
