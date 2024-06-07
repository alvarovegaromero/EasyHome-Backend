from venv import logger

from household_chores.models import AssignableTask, Task
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions.is_group_owner import IsGroupOwner
from ..serializers.assignable_task_serializer import AssignableTaskSerializer


class StartAssignableTasksAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def post(self, request, group_id):
        try:
            if AssignableTask.objects.filter(task__group_id=group_id).exists():
                return Response(
                    {"error": "Assignable tasks already started for the group"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not Task.objects.filter(group_id=group_id).exists():
                return Response(
                    {"error": "No tasks found for the group"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            tasks = Task.objects.filter(group_id=group_id)

            assignable_tasks = []
            for task in tasks:
                assignable_task = AssignableTask(task=task)
                assignable_task.save()
                assignable_tasks.append(assignable_task)

            serializer = AssignableTaskSerializer(assignable_tasks, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error("An error occurred during assignable tasks retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
