from venv import logger

from expense_distribution.models import Expense
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupSettlementView(APIView):
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

            expenses = Expense.objects.filter(group_id=group_id)

            return Response(Expense.getMinimumSettlements(expenses), status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during settlement retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
