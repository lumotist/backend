# Generated by Django 3.1.4 on 2021-01-16 11:56

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist', '0002_auto_20210116_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='animes',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), null=True, size=500),
        ),
    ]
