# Generated by Django 2.2.2 on 2019-07-23 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0013_auto_20190723_0436'),
    ]

    operations = [
        migrations.CreateModel(
            name='Amenity',
            fields=[
                ('amenity_id', models.AutoField(primary_key=True, serialize=False)),
                ('amenity_name', models.TextField(blank=True, null=True)),
            ],
        ),
    ]