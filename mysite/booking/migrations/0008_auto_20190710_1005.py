# Generated by Django 2.2.2 on 2019-07-10 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_auto_20190708_0253'),
    ]

    operations = [
        migrations.RenameField(
            model_name='room',
            old_name='room_number',
            new_name='num_guests',
        ),
        migrations.AddField(
            model_name='room',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]