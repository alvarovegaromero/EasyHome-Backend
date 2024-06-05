from django.contrib.auth.models import User
from household_chores.models import AssignableTask
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class AssignableTaskSerializer(serializers.ModelSerializer):
    assigned_user = UserSerializer(read_only=True)

    class Meta:
        model = AssignableTask
        fields = ["id", "task", "assigned_user", "is_completed", "date"]
