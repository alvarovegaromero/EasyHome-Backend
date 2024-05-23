from venv import logger

from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class GroupLeaveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response(
                    {"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                user_group = UserGroup.objects.get(
                    user=request.user, group=group)
            except UserGroup.DoesNotExist:
                return Response(
                    {"error": "You do not belong to this group."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            if group.owner == request.user:
                # If the user is the owner of the group, transfer ownership to
                # the next user
                next_owner_user_group = (
                    UserGroup.objects.filter(group=group)
                    .exclude(user=request.user)
                    .order_by("join_date")
                    .first()
                )

                if next_owner_user_group is None:
                    return Response(
                        {
                            "error": "You are the last member of the group. Please delete the group instead."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                group.owner = next_owner_user_group.user
                group.save()

            user_group.delete()

            return Response(
                {"success": "You have left the group successfully."},
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error("An error occurred during group left: %s" % str(e))
            return Response(
                "Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
