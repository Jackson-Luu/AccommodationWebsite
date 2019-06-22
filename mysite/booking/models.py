from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class User(models.Model):
    user_id = models.PositiveIntegerField(primary_key=True, null=False, blank=False, unique=True)
    username = models.TextField(unique=True, null=False, blank=False)
    password_hash = models.TextField(null=False, blank=False)
    first_name = models.TextField(null=False, blank=False)
    last_name = models.TextField(null=False, blank=False)
    birthday = models.DateField()
    description = models.TextField()

# class UserReviews(models.Model):
#     reviewer = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
#     reviewee = models.ForeignKey('User', to_field='user_id', on_delete=models.CASCADE)
#     rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)
#     text = models.TextField()

class Property(models.Model):
    # property_id = models.IntegerField(primary_key=True, blank=False, unique=True)
    title = models.TextField()
    size = models.DecimalField(max_digits=15, decimal_places=2)

# class Booking(models.Model):
#
#
# class room(models.Model):
