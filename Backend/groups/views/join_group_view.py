from venv import logger
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from groups.models import Group, UserGroup
from django.utils import timezone


class GroupJoinAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        join_code = request.data.get('joinCode')

        if not join_code:
            return Response({'error': 'Join code is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # group that have the provided join code and have not expired (join_code_expiration later) - only one.
            # maybe can be a function in the Group model
            group = Group.objects.filter(join_code=join_code, join_code_expiration__gt=timezone.now()).first() 

            if group is None:
                return Response({'error': 'Invalid or expired join code'}, status=status.HTTP_400_BAD_REQUEST)

            if UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response({'error': 'You are already a member of this group'}, status=status.HTTP_400_BAD_REQUEST)

            UserGroup.objects.create(user=request.user, group=group)

            return Response({'success': 'You have joined the group successfully.', 'id': group.id}, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.error("An error occurred during group join: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        