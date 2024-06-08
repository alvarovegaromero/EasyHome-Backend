from venv import logger

from household_chores.models import Task
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.permissions.is_group_owner import IsGroupOwner

from ..serializers.task_serializer import TaskSerializer


class TaskUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def put(self, request, group_id, task_id):
        try:
            try:
                task = Task.objects.get(id=task_id, group_id=group_id)
            except Task.DoesNotExist:
                return Response({"error": "Task wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if "title" not in request.data:
                return Response(
                    {"error": "The 'title' field is required."}, status=status.HTTP_400_BAD_REQUEST
                )

            task.title = request.data["title"]
            task.save()

            return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during task modification: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def delete(self, request, group_id, task_id):
        try:
            try:
                task = Task.objects.get(id=task_id, group_id=group_id)
            except Task.DoesNotExist:
                return Response({"error": "Task wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            logger.error("An error occurred during task deletion: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
