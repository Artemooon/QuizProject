# Generated by Django 3.0.6 on 2020-10-10 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_auto_20201002_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='image',
            field=models.ImageField(blank=True, upload_to='quiz_img/questions'),
        ),
    ]
