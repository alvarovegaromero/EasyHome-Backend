from venv import logger

from expense_distribution.serializers import ExpenseSerializer
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

            if not UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response(
                    {"error": "You are not a member of this group"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            expenses = group.get_expenses()
            serializer = ExpenseSerializer(expenses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during expulsion: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
