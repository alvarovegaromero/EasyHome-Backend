from django.contrib.auth.tokens import PasswordResetTokenGenerator
from users.models import UserProfile

token_generator = PasswordResetTokenGenerator()


def generate_token(user):
    return token_generator.make_token(user)


def associate_user_with_token(user, token, token_field):
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile.objects.create(user=user)

    setattr(user_profile, token_field, token)
    user_profile.save()
