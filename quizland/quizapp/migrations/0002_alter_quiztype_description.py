# Generated by Django 5.1.4 on 2025-01-10 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiztype',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
