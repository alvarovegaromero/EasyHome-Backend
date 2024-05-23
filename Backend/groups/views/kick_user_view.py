from venv import logger

from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from groups.models import Group, UserGroup


class GroupKickUserAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, group_id, user_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response(
                    {"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND
                )

            if not User.objects.filter(id=user_id).exists():
                return Response(
                    {"error": "User wasn't found"}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                user_group = UserGroup.objects.get(user_id=user_id, group_id=group_id)
            except UserGroup.DoesNotExist:
                return Response(
                    {"error": "User is not a member of this group"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if request.user != group.owner:
                return Response(
                    {"error": "Only the group owner can kick users"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if str(request.user.id) == user_id:
                return Response(
                    {"error": "You can not kick yourself. Leave the group instead"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                user_group.delete()

            return Response(
                {"success": "User has been succesfully kicked from the group"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error("An error occurred during expulsion: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
