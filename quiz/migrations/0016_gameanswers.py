# Generated by Django 3.0.6 on 2020-10-20 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_auto_20201020_0025'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameAnswers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(default='answer', max_length=100)),
                ('complete', models.BooleanField(verbose_name='Correct')),
                ('question_name', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='quiz.GameQuestions')),
            ],
        ),
    ]