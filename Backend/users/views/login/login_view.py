from venv import logger

from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class LoginAPIView(APIView):
    def post(self, request):
        try:
            username = request.data.get("username")
            password = request.data.get("password")

            if not username or not password:
                return Response(
                    {"error": "Username and password are required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {"token": token.key, "username": username, "id": user.id},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Incorrect username or password. Please, try again"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            logger.error("An error occurred during log in: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
