from django.db import models
from django.contrib.auth.models import Group

class SharedBoard(models.Model):
    group = models.OneToOneField(Group, on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    last_edited = models.DateTimeField(auto_now=True)