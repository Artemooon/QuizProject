# Generated by Django 3.0.6 on 2020-10-29 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_accounts', '0008_remove_profile_ban_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='scores_factor',
            field=models.PositiveSmallIntegerField(null=True),
        ),
    ]
