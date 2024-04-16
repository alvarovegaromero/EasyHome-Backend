from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from venv import logger
from .reset_password import reset_password_with_token

class ResetPasswordRequestAPIView(APIView):
    def post(self, request):
        try:
            token = request.data.get('token')
            new_password = request.data.get('new_password')
            confirm_password = request.data.get('confirm_password')

            if new_password != confirm_password:
                return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

            success, message = reset_password_with_token(token, new_password)
            if success:
                return Response({'success': message}, status=status.HTTP_200_OK)
            else:
                return Response({'error': message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error("An error occurred during password reset: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)