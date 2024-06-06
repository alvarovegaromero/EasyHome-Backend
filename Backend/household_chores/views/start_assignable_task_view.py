from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_owner import IsGroupOwner


class StartAssignableTasksAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def post(self, request, group_id):
        pass
