
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from users.models import UserTokenResetPassword

token_generator = PasswordResetTokenGenerator()

def generate_reset_password_token(user):
    return token_generator.make_token(user)

def generate_reset_url(user):
    token = generate_reset_password_token(user)

    associate_user_with_token(user, token)

    reset_url = reverse('reset-password-form') + f'?token={token}'
    return reset_url

def associate_user_with_token(user, token):
    try:
        user_profile = UserTokenResetPassword.objects.get(user=user)
    except UserTokenResetPassword.DoesNotExist:
        user_profile = UserTokenResetPassword.objects.create(user=user)

    user_profile.reset_password_token = token
    user_profile.save()

def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None

def reset_password_with_token(token, new_password):
    try:
        user_profile = UserTokenResetPassword.objects.get(reset_password_token=token)
        user = user_profile.user

        if token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return True, "Password reset successfully."
        else:
            return False, "Invalid token."
    except (UserTokenResetPassword.DoesNotExist, TypeError, ValueError, OverflowError):
        return False, "Invalid token."