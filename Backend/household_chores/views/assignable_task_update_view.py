from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember


class AssignableTaskUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def put(self, request, group_id, assignable_task_id):
        pass
