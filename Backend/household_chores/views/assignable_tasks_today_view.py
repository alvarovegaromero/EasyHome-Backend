from datetime import date, timedelta

from django.shortcuts import redirect
from django.urls import reverse
from household_chores.models import AssignableTask, Task
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember


class AssignableTasksTodayAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        last_date = (
            AssignableTask.objects.filter(task__group_id=group_id)
            .order_by("-date")
            .values("date")
            .first()
        )

        if last_date is None:
            return Response(
                {
                    "error": (
                        "For starting using assignable tasks, " "the owner must start the process"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        last_date = last_date["date"]
        today = date.today()

        if last_date is not today:
            tasks = Task.objects.filter(group_id=group_id)

            # Create an AssignableTask for each task for each day from the last date to today
            assignable_tasks = []
            current_date = last_date + timedelta(days=1)
            while current_date <= date.today():
                for task in tasks:
                    assignable_task = AssignableTask(task=task, date=current_date)
                    assignable_task.save()
                    assignable_tasks.append(assignable_task)
                current_date += timedelta(days=1)

        url = reverse("assignable_task_range", args=[group_id])
        url += f"?start_date={today}&end_date={today}"
        return redirect(url)
