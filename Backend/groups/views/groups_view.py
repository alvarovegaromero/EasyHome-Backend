from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from groups.models import UserGroup


class GroupsAPIView(APIView):
    permission_classes = (IsAuthenticated,) #Error 403

    def get_object(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise NotFound('A user with this ID does not exist.') #Error 404

    def get(self, request, user_id):
        user = self.get_object(user_id)

        if request.user != user:
            raise PermissionDenied('You do not have permission to access this user\'s groups.') #Error 403

        user_groups = UserGroup.objects.filter(user=user)  # get all UserGroup objects user
        group_data = [{'group_id': user_group.group.id, 
                        'group_name': user_group.group.name, 
                        'group_owner': user_group.group.owner.username}
                        for user_group in user_groups
                    ]  
        return Response({'groups': group_data}, status=status.HTTP_200_OK)
        