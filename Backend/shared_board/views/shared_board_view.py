from venv import logger

from groups.models import Group, UserGroup
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from shared_board.models import SharedBoard


class SharedBoardView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response(
                    {"error": "You do not belong to this group."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            new_content = request.data.get("content")
            if new_content is None:
                return Response(
                    {"error": "No content provided."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            board = SharedBoard.objects.get(group=group)

            # get request has to be done before
            last_edited = request.session.get("last_edited")
            if last_edited is not None and str(board.last_edited) != last_edited:
                return Response(
                    {"error": "The board has been edited by another user."},
                    status=status.HTTP_409_CONFLICT,
                )

            board.content = new_content
            board.save()

            request.session["last_edited"] = str(board.last_edited)

            return Response(
                {
                    "message": "Board content updated successfully.",
                    "content": board.content,
                },
                status=status.HTTP_200_OK,
            )

        except Exception as e:
            logger.error("An error occurred during shared board edition: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    def get(self, request, group_id):
        try:
            try:
                group = Group.objects.get(id=group_id)
            except Group.DoesNotExist:
                return Response({"error": "Group wasn't found"}, status=status.HTTP_404_NOT_FOUND)

            if not UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response(
                    {"error": "You do not belong to this group."},
                    status=status.HTTP_403_FORBIDDEN,
                )

            board = SharedBoard.objects.get(group=group)
            request.session["last_edited"] = str(board.last_edited)
            return Response({"data": board.content}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during shared board retrieval: %s" % str(e))
            return Response(
                {"error": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
