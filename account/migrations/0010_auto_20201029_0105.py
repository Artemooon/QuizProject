# Generated by Django 3.0.6 on 2020-10-29 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_accounts', '0009_profile_scores_factor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='scores_factor',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
