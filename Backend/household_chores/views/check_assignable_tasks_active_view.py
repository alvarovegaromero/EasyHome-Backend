from venv import logger

from household_chores.models import AssignableTask
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember


class CheckAssignableTasksActiveAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        try:
            assignable_task_exists = AssignableTask.objects.filter(task__group_id=group_id).exists()

            return Response({"active": assignable_task_exists})
        except Exception as e:
            logger.error("An error occurred during assignable tasks retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
