from venv import logger

from expense_distribution.models import Expense
from expense_distribution.serializers import ExpenseDetailSerializer
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class ExpenseDetailView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id, expense_id):
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

            try:
                expense = Expense.objects.get(id=expense_id, group=group)
            except Expense.DoesNotExist:
                return Response({"error": "Expense wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = ExpenseDetailSerializer(expense)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during expense retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, group_id, expense_id):
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

            try:
                expense = Expense.objects.get(id=expense_id, group=group)
            except Expense.DoesNotExist:
                return Response({"error": "Expense wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            expense.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error("An error occurred during expense deletion: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
