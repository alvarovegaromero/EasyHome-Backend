from datetime import date

from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from utils.permissions.is_group_member import IsGroupMember


class AssignableTasksTodayAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        today = date.today()
        url = reverse("assignable_task_range", args=[group_id])
        url += f"?start_date={today}&end_date={today}"
        return redirect(url)
