from venv import logger

from requests import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember


class AssignableTaskUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def put(self, request, group_id, assignable_task_id):
        try:
            pass
        except Exception as e:
            logger.error("An error occurred during assignable task update: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
