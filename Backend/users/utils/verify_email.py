from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from users.models import UserProfile

token_generator = PasswordResetTokenGenerator()


def generate_token(user):
    return token_generator.make_token(user)


def generate_reset_url(user):
    token = generate_token(user)
    associate_user_with_token(user, token, "reset_password_token")
    reset_url = reverse("reset-password-form") + f"?token={token}"
    return reset_url


def associate_user_with_token(user, token, token_field):
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    setattr(user_profile, token_field, token)
    user_profile.save()


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None


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
