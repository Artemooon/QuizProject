# Generated by Django 3.0.6 on 2020-10-20 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_gameanswers'),
    ]

    operations = [
        migrations.AddField(
            model_name='answers',
            name='quiz_name',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.Quizzes'),
        ),
    ]