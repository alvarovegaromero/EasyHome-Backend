from venv import logger

from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutAPIView(APIView):
    def post(self, request):
        try:
            if request.user.is_authenticated:
                # Delete the token when the user logout - Safer but costly.
                # request.user.auth_token.delete()
                logout(request)
                return Response(
                    {"success": "Logout successful"}, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "User is not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            logger.error("An error occurred during log out: %s" % str(e))
            return Response("Internal Server Error",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
