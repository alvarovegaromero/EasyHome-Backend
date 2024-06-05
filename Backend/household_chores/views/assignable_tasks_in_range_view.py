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
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        is_completed = request.query_params.get("is_completed")

        if not start_date or not end_date:
            return Response(
                {"error": "Both 'start_date' and 'end_date' are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        start_date = parse_date(start_date)
        end_date = parse_date(end_date)

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

        tasks = AssignableTask.objects.filter(**filters)

        serializer = AssignableTaskSerializer(tasks, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
