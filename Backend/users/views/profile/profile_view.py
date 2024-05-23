from venv import logger

from django.contrib.auth.models import User
from django.core.validators import validate_email
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ProfileAPIView(APIView):
    def get(self, request):
        try:
            if request.user.is_authenticated:
                return Response(
                    {
                        "username": request.user.username,
                        "email": request.user.email,
                        "firstName": request.user.first_name,
                        "lastName": request.user.last_name,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "User is not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            logger.error("An error occurred during profile retrieval: %s" % str(e))
            return Response(
                "Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def post(self, request):
        try:
            if request.user.is_authenticated:
                user = request.user
                username = request.data.get("username")
                email = request.data.get("email")
                first_name = request.data.get("firstName", "")
                last_name = request.data.get("lastName", "")

                if not username:
                    return Response(
                        {"error": "Username is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if not email:
                    return Response(
                        {"error": "Email is required"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if username != user.username:
                    if User.objects.filter(username=username).exists():
                        return Response(
                            {"error": "Username already in use"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    user.username = username

                if email != user.email:
                    if (
                        User.objects.filter(email=email)
                        .exclude(username=user.username)
                        .exists()
                    ):
                        return Response(
                            {"error": "Email already in use"},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                try:
                    validate_email(email)
                except BaseException:
                    return Response(
                        {"error": "Invalid email format"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.email = email
                user.first_name = first_name
                user.last_name = last_name
                user.save()

                return Response(
                    {"success": "Profile updated successfully"},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "User is not authenticated"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            logger.error("An error occurred during profile update: %s" % str(e))
            return Response(
                "Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
