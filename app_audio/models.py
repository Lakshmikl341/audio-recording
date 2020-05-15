from django.db import models
class Customer(models.Model):

    audio = models.FileField(upload_to='audio/', null=True, blank=True)