from django.db import models

# Create your models here.
class Property(models.Model):
    title = models.TextField()
    size = models.DecimalField(max_digits=15, decimal_places=2)


