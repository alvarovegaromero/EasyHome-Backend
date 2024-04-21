from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status

class GroupsAPIView(APIView):
    def get(self, request, user_id):
        print('User ID:', user_id)
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND) 
        
        print('User name:', user.username)

        data = {
            'message': 'Hello from GroupsAPIView!',
            'data': {
                'group_id': 1,
                'group_name': 'Dummy Group'
            }
        }

        return Response(data)