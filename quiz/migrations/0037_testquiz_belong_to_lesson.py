# Generated by Django 2.1.7 on 2019-06-29 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0036_auto_20190629_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='testquiz',
            name='belong_to_lesson',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='quiz.Lesson'),
        ),
    ]
