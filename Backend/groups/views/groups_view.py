from rest_framework.views import APIView
from rest_framework.response import Response

class GroupsAPIView(APIView):
    def get(self, request):
        data = {
            'message': 'Hello from GroupsAPIView!',
            'data': {
                'group_id': 1,
                'group_name': 'Dummy Group'
            }
        }
        return Response(data)