from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass
    birthday = models.DateField(null=True)
    description = models.TextField(null=True)
    user_id = models.AutoField(primary_key=True)