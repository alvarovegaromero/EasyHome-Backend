from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


class TaskListCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        pass

    def post(self, request, group_id):
        pass
