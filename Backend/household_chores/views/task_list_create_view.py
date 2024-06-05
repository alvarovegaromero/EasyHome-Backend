from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_owner import IsGroupOwner


class TaskListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def get(self, request, group_id):
        pass

    def post(self, request, group_id):
        pass
