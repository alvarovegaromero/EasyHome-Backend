from django.contrib.auth.models import User
from django.db import models


class UserTokenResetPassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=100, blank=True, null=True)

    # TO DO: Add token expiration
    #
    # token_expiration = models.DateTimeField(blank=True, null=True)
    # def is_token_valid(self):
    #    return self.token_expiration > timezone.now()
