from django.db import models


class SharedBoard(models.Model):
    group = models.OneToOneField('groups.Group', on_delete=models.CASCADE)
    content = models.TextField(blank=True)
    last_edited = models.DateTimeField(auto_now=True)
