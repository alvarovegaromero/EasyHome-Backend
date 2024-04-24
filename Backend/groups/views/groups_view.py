from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from groups.models import UserGroup


class GroupsAPIView(APIView):
    permission_classes = (IsAuthenticated,) #Error 403

    def get(self, request):
        try:
            user_groups = UserGroup.objects.filter(user=request.user)  
            group_data = [{'group_id': user_group.group.id, 
                            'group_name': user_group.group.name, 
                            'group_owner': user_group.group.owner.username}
                            for user_group in user_groups
                        ]
            if not group_data:
                return Response({'message': 'No groups found for this user.'}, status=status.HTTP_200_OK)
            return Response({'groups': group_data}, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error("An error occurred during group retrieval: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)