from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class AssignableTaskUpdateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, group_id, assignable_task_id):
        pass
