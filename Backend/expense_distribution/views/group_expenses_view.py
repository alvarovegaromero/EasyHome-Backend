from venv import logger

from expense_distribution.serializers import (
    ExpenseDetailSerializer,
    ExpensePostSerializer,
    ExpensesGetSerializer,
)
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupExpensesView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.is_member(request.user, group):
                return Response(
                    {"error": "You are not a member of this group"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            expenses = group.get_expenses()
            serializer = ExpensesGetSerializer(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during expenses retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.is_member(request.user, group):
                return Response(
                    {"error": "You are not a member of this group"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            data = request.data.copy()  # Make a mutable copy
            data["group"] = group_id

            serializer = ExpensePostSerializer(data=data)
            if serializer.is_valid():
                expense = serializer.save()

                expense_serializer = ExpenseDetailSerializer(expense)

                return Response(
                    {"success": expense.id, "expense": expense_serializer.data},
                    status=status.HTTP_201_CREATED,
                )

            first_error_message = next(iter(serializer.errors.values()))[0]
            return Response({"error": first_error_message}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error("An error occurred during expense creation: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
