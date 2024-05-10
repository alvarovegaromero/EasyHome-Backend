from venv import logger
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from groups.models import Group, UserGroup


class GroupGenerateCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, group_id):
        group = get_object_or_404(Group, pk=group_id)

        try:
            if not UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response({'error': 'You are not a member of this group.'}, status=status.HTTP_403_FORBIDDEN)

            if group.join_code and group.join_code_expiration > timezone.now():
                join_code = group.join_code
            else:
                join_code = group.generate_join_code()

            return Response({'join_code': join_code}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during group join code generation: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
