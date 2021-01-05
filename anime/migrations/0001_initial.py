# Generated by Django 3.1.4 on 2021-01-05 12:14

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=156)),
                ('source', models.CharField(max_length=145)),
                ('anime_type', models.CharField(db_index=True, max_length=7)),
                ('num_episodes', models.IntegerField(db_index=True)),
                ('status', models.CharField(db_index=True, max_length=9)),
                ('year', models.IntegerField(db_index=True)),
                ('picture', models.CharField(max_length=168)),
                ('tags', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=27), db_index=True, size=None)),
            ],
        ),
    ]
