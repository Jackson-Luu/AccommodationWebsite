# Generated by Django 2.2.2 on 2019-08-04 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0004_auto_20190803_0052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='photo',
            field=models.URLField(blank=True),
        ),
    ]
