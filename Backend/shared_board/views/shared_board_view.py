from venv import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

class SharedBoardView(APIView):
    permission_classes = (IsAuthenticated,) 

    def post(self, request):
        try:
            pass
        except Exception as e:
            logger.error("An error occurred during shared board edition: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            pass
        except Exception as e:
            logger.error("An error occurred during shared board retrieval: %s" % str(e))
            return Response({'error': "Internal Server Error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)