from venv import logger

from household_chores.models import Task
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.permissions.is_group_owner import IsGroupOwner

from ..serializers.task_serializer import TaskSerializer


class TaskListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def get(self, request, group_id):
        try:
            tasks = Task.objects.filter(group_id=group_id)

            serializer = TaskSerializer(tasks, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during tasks retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def post(self, request, group_id):
        try:
            if "title" not in request.data or request.data["title"].strip() == "":
                return Response(
                    {"error": "The 'title' field is required."}, status=status.HTTP_400_BAD_REQUEST
                )

            task = Task.objects.create(title=request.data["title"].strip(), group_id=group_id)

            return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error("An error occurred during task creation: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
