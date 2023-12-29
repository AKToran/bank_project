from django.db import models

# Create your models here.
class Bank(models.Model):
    is_bankrupt = models.BooleanField(default=False)