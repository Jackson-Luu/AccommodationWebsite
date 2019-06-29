from django.db import models
# from user_manager.models import CustomUser

# class User(models.Model):
#     user_id = models.PositiveIntegerField(primary_key=True, null=False, blank=False, unique=True)
#     username = models.TextField(unique=True, null=False, blank=False)
#     password_hash = models.TextField(null=False, blank=False)
#     first_name = models.TextField(null=False, blank=False)
#     last_name = models.TextField(null=False, blank=False)
#     birthday = models.DateField()
#     description = models.TextField()

class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    # uncomment when user login implemented
    # host_id = models.ForeignKey('CustomUser', to_field='user_id', on_delete=models.CASCADE, default=-1)
    name = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    size = models.PositiveSmallIntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    bookable = models.BooleanField(null=False, blank=False, default=False)

class Room(models.Model):
    room_id = models.AutoField(primary_key=True)
    property_id = models.ForeignKey('Property', to_field='property_id', on_delete=models.CASCADE)
    room_number = models.IntegerField(null=True, blank=True)

class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('user_manager.CustomUser', to_field='user_id', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

class BookingTable(models.Model):
    booking = models.ForeignKey('Booking', to_field='booking_id', on_delete=models.CASCADE)
    room = models.ForeignKey('Room', to_field='room_id', on_delete=models.CASCADE)
