# Generated by Django 2.2.2 on 2019-08-03 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0015_propertyamenities'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='bookable',
            field=models.BooleanField(default=True),
        ),
    ]
