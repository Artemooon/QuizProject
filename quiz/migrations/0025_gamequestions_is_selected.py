# Generated by Django 3.0.6 on 2020-10-24 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0024_auto_20201023_2123'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamequestions',
            name='is_selected',
            field=models.BooleanField(null=True),
        ),
    ]