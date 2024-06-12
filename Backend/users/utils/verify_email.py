from django.urls import reverse
from users.models import UserProfile
from utils.functions.send_mail import send_email

from Backend.settings import BASE_URL

from .token_manager import associate_user_with_token, generate_token, token_generator


def generate_email_verification_url(user):
    token = generate_token(user)
    associate_user_with_token(user, token, "email_verification_token")
    verification_url = reverse("email-verification") + f"?token={token}"
    return BASE_URL + verification_url


def verify_email_with_token(token):
    try:
        user_profile = UserProfile.objects.get(email_verification_token=token)
        user = user_profile.user

        if token_generator.check_token(user, token):
            user_profile.has_email_verified = True
            user_profile.save()
            return True, "Email verified successfully."
        else:
            return False, "Invalid token. The token is not valid for verifying the email."
    except (UserProfile.DoesNotExist, TypeError, ValueError, OverflowError):
        return False, "Invalid token. The token provided does not exist or is malformed."


def send_email_verification_email(user, verification_url):
    subject = "Email Verification (EasyHome)"
    message = (
        "Hi "
        + user.username
        + "\n\n"
        + "Please click the following link to verify your email: "
        + verification_url
        + "\n\n"
        + "Best regards,\n"
        + "The EasyHome Team"
    )
    send_email(subject, message, user.email)
