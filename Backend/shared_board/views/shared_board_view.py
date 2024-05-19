from venv import logger
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from groups.models import Group, UserGroup
from shared_board.models import SharedBoard

class SharedBoardView(APIView):
    permission_classes = (IsAuthenticated,) 

    def post(self, request, group_id):
        try:
            pass
        except Exception as e:
            logger.error("An error occurred during shared board edition: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, group_id):
        try:
            group = get_object_or_404(Group, pk=group_id)

            if not UserGroup.objects.filter(user=request.user, group=group).exists():
                return Response({'error': 'You do not belong to this group.'}, status=status.HTTP_403_FORBIDDEN)                
                
            board = SharedBoard.objects.get(group=group)
            request.session['last_edited'] = str(board.last_edited)
            return Response({'data': board.content}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during shared board retrieval: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)