from venv import logger

from django.contrib.auth.models import User
from django.db import transaction
from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupChangeOwnerAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, group_id, user_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group wasn't found"},
                                status=status.HTTP_404_NOT_FOUND)

            try:
                new_owner = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return Response({"error": "User wasn't found"},
                                status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.objects.filter(
                user_id=user_id, group_id=group_id
            ).exists():
                return Response(
                    {"error": "User is not a member of this group"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            if request.user != group.owner:
                return Response(
                    {"error": "Only the group owner can change ownership"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if str(request.user.id) == user_id:
                return Response(
                    {"error": "You are already the owner of the group"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            with transaction.atomic():
                group.owner = new_owner
                group.save()

            return Response(
                {"success": "Ownership of the group has been changed succesfully"},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error(
                "An error occurred during ownership change: %s" %
                str(e))
            return Response("Internal Server Error",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
