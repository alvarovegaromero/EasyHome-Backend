from venv import logger

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView


class MyInfoTokenAPIView(APIView):
    def get(self, request):
        try:
            token_key = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]

            try:
                token = Token.objects.get(key=token_key)
            except Token.DoesNotExist:
                return Response("Invalid token", status=status.HTTP_401_UNAUTHORIZED)

            user = token.user

            return Response({"id": user.id, "username": user.username}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error("An error occurred during user information retrieval: %s" % str(e))
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
