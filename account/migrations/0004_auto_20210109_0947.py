# Generated by Django 3.1.4 on 2021-01-09 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20210109_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created',
            field=models.DateTimeField(default='YYYY-MM-DD HH:MM'),
        ),
    ]
