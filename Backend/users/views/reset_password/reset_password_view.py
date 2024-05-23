from venv import logger

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Backend.settings import BASE_URL

from .reset_password import generate_reset_url, get_user_by_email


class ResetPasswordAPIView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            user = get_user_by_email(email)

            if user is None:
                return Response({"error": "User not found"},
                                status=status.HTTP_404_NOT_FOUND)

            reset_url = generate_reset_url(user)
            reset_url = BASE_URL + reset_url

            subject = "Password Reset (EasyHome)"
            from_email = "easyhome.applicationhelp@gmail.com"
            to_email = [email]
            message = (
                "Hi "
                + user.username
                + "\n\n"
                + "The link for resetting your password is: "
                + reset_url
                + "\n\n"
                + "Best regards,\n"
                + "EasyHome Team"
            )

            send_mail(
                subject,
                message,
                from_email,
                to_email,
                fail_silently=False)
            return Response(
                {"success": "Email sent succesfully"}, status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.error(
                "An error occurred during sending the "
                + "resetting password email: %s" % str(e)
            )
            return Response("Internal Server Error",
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
