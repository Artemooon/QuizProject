# Generated by Django 3.0.6 on 2020-10-02 21:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0007_auto_20200929_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='comments_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='comments_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
