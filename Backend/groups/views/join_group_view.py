from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from groups.models import Group, UserGroup
from django.utils import timezone


class GroupJoinAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        join_code = request.data.get('joinCode')

        if not join_code:
            return Response({'error': 'Join code is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the group with the provided join code that has not expired
        groups = Group.objects.filter(join_code=join_code, join_code_expiration__gt=timezone.now())
        group = groups.order_by('-join_code_expiration').first()

        if group is None:
            return Response({'error': 'Invalid or expired join code'}, status=status.HTTP_400_BAD_REQUEST)

        if UserGroup.objects.filter(user=request.user, group=group).exists():
            return Response({'error': 'You are already a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

        UserGroup.objects.create(user=request.user, group=group)

        return Response({'success': 'You have joined the group successfully.'}, status=status.HTTP_200_OK)