from venv import logger

from groups.models import UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupsAPIView(APIView):
    permission_classes = (IsAuthenticated,)  # Error 403

    def get(self, request):
        try:
            user_groups = UserGroup.objects.filter(user=request.user)
            group_data = [
                {"id": user_group.group.id, "name": user_group.group.name}
                for user_group in user_groups
            ]

            return Response({"groups": group_data}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(
                "An error occurred during groups retrieval: %s" %
                str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
