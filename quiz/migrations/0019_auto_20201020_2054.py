# Generated by Django 3.0.6 on 2020-10-20 20:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0018_auto_20201020_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameanswers',
            name='is_used',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='gamequestions',
            name='is_used',
            field=models.BooleanField(),
        ),
    ]
