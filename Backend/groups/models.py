import secrets
import string
from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from shared_board.models import SharedBoard

from .currency_choices import CURRENCY_CHOICES


class Group(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField(blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES)
    creation_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_groups"
    )  # accesible using user.owned_groups
    join_code = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True)
    join_code_expiration = models.DateTimeField(null=True, blank=True)

    def generate_join_code(self):
        alphabet = string.ascii_letters + string.digits  # generate letters and digits
        while True:
            join_code = "".join(secrets.choice(alphabet) for i in range(30))
            # Check if the generated code already exists and if it has expired.
            # If no, break the loop
            if not Group.objects.filter(
                join_code=join_code, join_code_expiration__gt=timezone.now()
            ).exists():
                self.join_code = join_code
                break
        self.join_code_expiration = timezone.now() + timedelta(weeks=1)
        self.save()
        return self.join_code

    def get_users(self):
        return [
            {
                "username": user_group.user.username,
                "id": user_group.user.id,
                "is_owner": user_group.user == self.owner,
            }
            for user_group in self.usergroup_set.all()
        ]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # If this is a new group (i.e., it doesn't have an ID yet),
        # we'll create a UserGroup entry after saving. - To ensure the owner is
        # a member of the group
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            UserGroup.objects.create(user=self.owner, group=self)
            SharedBoard.objects.create(group=self)


class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "group"], name="unique_usergroup"
            )  # Unique user-group pair
        ]

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
