from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
	pass
	birthday = models.DateField(null=True, blank=True)
	description = models.TextField(null=True, blank=True)
	user_id = models.AutoField(primary_key=True)
	photo = models.URLField(blank=True)


class PropertyOwnership(models.Model):
	owner = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE)
	property = models.ForeignKey('booking.property', to_field='property_id', on_delete=models.CASCADE)


class PropertyFavourites(models.Model):
	user = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE)
	property = models.ForeignKey('booking.property', to_field='property_id', on_delete=models.CASCADE)
