# Generated by Django 2.2.2 on 2019-07-23 04:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0012_image_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='propertyamenities',
            name='amenity',
        ),
        migrations.RemoveField(
            model_name='propertyamenities',
            name='property',
        ),
        migrations.DeleteModel(
            name='Amenity',
        ),
        migrations.DeleteModel(
            name='PropertyAmenities',
        ),
    ]