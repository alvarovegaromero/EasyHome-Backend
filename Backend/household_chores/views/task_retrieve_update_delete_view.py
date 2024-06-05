from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class TaskRetrieveUpdateDeleteAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id, task_id):
        pass

    def put(self, request, group_id, task_id):
        pass

    def delete(self, request, group_id, task_id):
        pass
