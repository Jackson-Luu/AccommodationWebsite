# Generated by Django 2.2.2 on 2019-07-02 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0002_propertyfavourites_propertyownership'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birthday',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]