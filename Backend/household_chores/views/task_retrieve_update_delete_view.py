from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from ..permissions.is_group_owner import IsGroupOwner


class TaskRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated, IsGroupOwner)

    def get(self, request, group_id, task_id):
        pass

    def put(self, request, group_id, task_id):
        pass

    def delete(self, request, group_id, task_id):
        pass
