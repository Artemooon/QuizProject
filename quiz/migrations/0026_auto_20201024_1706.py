# Generated by Django 3.0.6 on 2020-10-24 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0025_gamequestions_is_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamequestions',
            name='is_selected',
        ),
        migrations.AddField(
            model_name='gameanswers',
            name='is_selected',
            field=models.BooleanField(null=True),
        ),
    ]
