# Generated by Django 3.0.6 on 2020-10-24 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0026_auto_20201024_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameanswers',
            name='is_selected',
            field=models.BooleanField(),
        ),
    ]
