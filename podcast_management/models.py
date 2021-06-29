from django.db import models


class Podcast(models.Model):
    file = models.FileField(upload_to='podcast', null=True)
    request = models.OneToOneField("request_management.", on_delete=models.CASCADE)
    delivery_date = models.DateField(null=True)
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)

