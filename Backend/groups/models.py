from django.db import models
from django.contrib.auth.models import User
from .currency_choices import currency_choices

class Group(models.Model):
    name = models.CharField(max_length=35)
    description = models.TextField()
    currency = models.CharField(max_length=3, choices=currency_choices)
    creation_date = models.DateField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_groups') # accesible using user.owned_groups

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # If this is a new group (i.e., it doesn't have an ID yet), 
        # we'll create a UserGroup entry after saving. - To ensure the owner is a member of the group
        is_new = self.pk is None

        super().save(*args, **kwargs)

        if is_new:
            UserGroup.objects.create(user=self.owner, group=self)

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    join_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'group'], name='unique_usergroup') # Unique user-group pair
        ]

    def __str__(self):
        return f"{self.user.username} - {self.group.name}"
