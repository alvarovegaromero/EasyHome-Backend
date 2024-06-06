from venv import logger

from household_chores.models import AssignableTask
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember
from ..serializers.assignable_task_serializer import AssignableTaskSerializer


class AssignableTaskUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def put(self, request, group_id, assignable_task_id):
        try:
            try:
                assignable_task = AssignableTask.objects.get(id=assignable_task_id)
            except AssignableTask.DoesNotExist:
                return Response(
                    {"error": "Assignable task wasn't found"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if assignable_task.task.group.id != group_id:
                return Response(
                    {"error": "This task doesn't belong to this group."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if assignable_task.is_completed or assignable_task.assigned_user is not None:
                return Response(
                    {"error": "This task is already completed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            assignable_task.is_completed = True
            assignable_task.assigned_user = request.user
            assignable_task.save()

            serializer = AssignableTaskSerializer(assignable_task)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during assignable task update: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
