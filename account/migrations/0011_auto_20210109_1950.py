# Generated by Django 3.1.4 on 2021-01-09 19:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.CharField(default='https://davidnelsoncollins.com/wp-content/uploads/2018/11/profiles-empty1.png', max_length=77),
        ),
    ]
