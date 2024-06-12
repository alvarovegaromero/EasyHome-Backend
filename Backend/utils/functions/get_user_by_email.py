from django.contrib.auth.models import User


def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None
