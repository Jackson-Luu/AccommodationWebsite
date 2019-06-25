from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    pass
    birthday = models.DateField(null=True)
    description = models.TextField(null=True)
    user_id = models.AutoField(primary_key=True)

# class User(models.Model):
#     user_id = models.PositiveIntegerField(primary_key=True, null=False, blank=False, unique=True)
#     username = models.TextField(unique=True, null=False, blank=False)
#     password_hash = models.TextField(null=False, blank=False)
#     first_name = models.TextField(null=False, blank=False)
#     last_name = models.TextField(null=False, blank=False)
#     birthday = models.DateField()
#     description = models.TextField()

# class UserReviews(models.Model):
#     reviewer = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
#     reviewee = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)
#     text = models.TextField()

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    #host_id = models.ForeignKey('CustomUser', to_field='user_id', on_delete=models.CASCADE, null=True, blank=True, default=-1) 
    #change back to null=false , blank=false
    name = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    size = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bookable = models.BooleanField(null=False, blank=False, default=False)


# class Booking(models.Model):
#
#
# class room(models.Model):
