from django.utils import timezone


def current_date():
    return timezone.now().date()
