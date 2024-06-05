from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_member import IsGroupMember


class AssignableTasksTodayAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupMember)

    def get(self, request, group_id):
        pass
