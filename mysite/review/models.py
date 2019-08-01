from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class UserReviews(models.Model):
    reviewer = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE, related_name='reviewer')
    reviewee = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE, related_name='reviewee')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False, blank=False)
    text = models.TextField(null=True, blank=True)

class PropertyReviews(models.Model):
    reviewer = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE)
    reviewee = models.ForeignKey('booking.Property', to_field='property_id', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=False,blank=False)
    text = models.TextField(null=True, blank=True)