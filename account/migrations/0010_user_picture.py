# Generated by Django 3.1.4 on 2021-01-09 17:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20210109_1006'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.CharField(default=django.utils.timezone.now, max_length=72),
            preserve_default=False,
        ),
    ]
