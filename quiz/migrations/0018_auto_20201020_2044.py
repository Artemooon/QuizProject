# Generated by Django 3.0.6 on 2020-10-20 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quiz', '0017_answers_quiz_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='gameanswers',
            name='is_used',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='gameanswers',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='gamequestions',
            name='is_used',
            field=models.BooleanField(null=True),
        ),
        migrations.AddField(
            model_name='gamequestions',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]