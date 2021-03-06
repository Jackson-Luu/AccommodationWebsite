# Generated by Django 2.2.2 on 2019-07-06 13:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='host_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='booking',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Booking'),
        ),
        migrations.AddField(
            model_name='bookingtable',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booking.Room'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
