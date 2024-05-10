from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.response import Response
from django.db import transaction


class GroupKickUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, group_id, user_id):

        try:
            group = Group.objects.get(id=group_id)
        except Group.DoesNotExist:
            return Response("Group wasn't found", status=status.HTTP_404_NOT_FOUND)

        try:
            user_group = UserGroup.objects.get(user_id=user_id, group_id=group_id)
        except UserGroup.DoesNotExist:
            return Response("User is not a member of this group", status=status.HTTP_404_NOT_FOUND)

        if request.user != group.owner:
            return Response("Only the group owner can kick users", status=status.HTTP_403_FORBIDDEN)

        if request.user.id == user_id:
            return Response("You can not kick yourself. Leave the group instead", status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            user_group.delete()

        return Response("User has been succesfully kicked from the group", status=status.HTTP_200_OK)
    