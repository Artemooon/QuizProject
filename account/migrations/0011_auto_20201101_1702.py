# Generated by Django 3.0.6 on 2020-11-01 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_accounts', '0010_auto_20201029_0105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='rank',
            field=models.CharField(choices=[('Academy Student', 'academy'), ('Genin', 'genin'), ('Chuunin', 'chuunin'), ('Jounin', 'jounin'), ('ANBU', 'anbu'), ('Sannin', 'sannin'), ('Kage', 'kage'), ('NARUTO', 'NARUTO')], default='Academy Student', max_length=40),
        ),
    ]