# Generated by Django 2.2.2 on 2019-06-25 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('property_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('location', models.TextField(blank=True, null=True)),
                ('size', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('bookable', models.BooleanField(default=False)),
            ],
        ),
    ]
