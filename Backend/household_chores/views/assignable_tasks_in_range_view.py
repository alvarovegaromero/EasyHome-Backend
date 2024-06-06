from datetime import timedelta
from venv import logger

from django.utils.dateparse import parse_date
from household_chores.models import AssignableTask
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember
from ..serializers.assignable_task_serializer import AssignableTaskSerializer


class AssignableTasksInRangeAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        try:
            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")
            is_completed = request.query_params.get("is_completed")  # Optional
            user_id = request.query_params.get("user_id")  # Optional

            if not start_date or not end_date:
                return Response(
                    {"error": "Both 'start_date' and 'end_date' are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
            end_date = (
                end_date + timedelta(days=1) - timedelta(seconds=1)
            )  # Set end_date to 23:59:59

            if not start_date or not end_date:
                return Response(
                    {"error": "Invalid date format. Use 'YYYY-MM-DD'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if start_date > end_date:
                return Response(
                    {"error": "'start_date' must be before 'end_date'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            filters = {"task__group_id": group_id, "date__range": [start_date, end_date]}

            if is_completed is not None:
                filters["is_completed"] = is_completed.lower() == "true"

            if user_id is not None:
                if is_completed is False:
                    return Response(
                        {
                            "error": (
                                "'is_completed' can not be set to false "
                                "when 'user_id' is provided."
                            )
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                filters["assigned_user_id"] = user_id

            tasks = AssignableTask.objects.filter(**filters)

            serializer = AssignableTaskSerializer(tasks, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("An error occurred during assignable tasks retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
