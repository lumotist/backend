# Generated by Django 3.1.4 on 2021-01-10 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_user_receive_emails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='receive_emails',
            field=models.BooleanField(default=False),
        ),
    ]
