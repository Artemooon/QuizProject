# Generated by Django 3.0.6 on 2020-09-29 21:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quizzes',
            name='publucation_time',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 9, 29, 21, 35, 10, 966833), null=True),
        ),
        migrations.AlterField(
            model_name='quizzresult',
            name='result_time',
            field=models.DateTimeField(default=datetime.datetime(2020, 9, 29, 21, 35, 10, 969854), null=True),
        ),
    ]
