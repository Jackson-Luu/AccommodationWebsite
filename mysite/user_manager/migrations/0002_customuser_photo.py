# Generated by Django 2.2.2 on 2019-08-02 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_manager', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='photo',
            field=models.CharField(default='https://www.materialui.co/materialIcons/social/person_grey_192x192.png', max_length=255),
        ),
    ]