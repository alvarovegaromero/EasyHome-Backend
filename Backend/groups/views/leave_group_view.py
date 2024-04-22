from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from groups.models import Group, UserGroup

class GroupLeaveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)
        user_group = get_object_or_404(UserGroup, user=request.user, group=group)

        if group.owner == request.user:
            # If the user is the owner of the group, transfer ownership to the next user
            next_owner_user_group = UserGroup.objects.filter(group=group).exclude(user=request.user).order_by('join_date').first()

            if next_owner_user_group is None:
                return Response({'error': 'You are the last member of the group. Please delete the group instead.'}, status=status.HTTP_400_BAD_REQUEST)

            group.owner = next_owner_user_group.user
            group.save()

        user_group.delete()

        return Response({'success': 'You have left the group successfully.'}, status=status.HTTP_200_OK)