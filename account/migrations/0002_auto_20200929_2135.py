# Generated by Django 3.0.6 on 2020-09-29 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedbackmodel',
            name='send_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 29, 21, 35, 10, 973844), null=True),
        ),
    ]
