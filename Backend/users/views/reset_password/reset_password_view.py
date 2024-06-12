from venv import logger

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.functions.get_user_by_email import get_user_by_email

from ...utils.reset_password import (
    generate_reset_password_url,
    send_password_reset_email,
)


class ResetPasswordAPIView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            user = get_user_by_email(email)

            if user is None:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            reset_url = generate_reset_password_url(user)
            send_password_reset_email(user, reset_url)

            return Response({"success": "Email sent succesfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(
                "An error occurred during sending the " + "resetting password email: %s" % str(e)
            )
            return Response("Internal Server Error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
