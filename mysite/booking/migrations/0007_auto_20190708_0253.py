# Generated by Django 2.2.2 on 2019-07-07 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0006_booking_num_guests'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='property_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='booking.Property'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='booking',
            name='num_guests',
            field=models.IntegerField(default=1),
        ),
    ]
