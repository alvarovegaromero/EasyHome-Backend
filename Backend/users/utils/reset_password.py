from django.urls import reverse
from users.models import UserProfile

from .token_manager import associate_user_with_token, generate_token, token_generator


def generate_reset_password_url(user):
    token = generate_token(user)
    associate_user_with_token(user, token, "reset_password_token")
    reset_url = reverse("reset-password-form") + f"?token={token}"
    return reset_url


def reset_password_with_token(token, new_password):
    try:
        user_profile = UserProfile.objects.get(reset_password_token=token)
        user = user_profile.user

        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return True, "Password changed successfully."
        else:
            return False, ("Invalid token. " "The token is not valid for resetting the password.")
    except (UserProfile.DoesNotExist, TypeError, ValueError, OverflowError):
        return False, ("Invalid token." "The token provided does not exist or is malformed.")
