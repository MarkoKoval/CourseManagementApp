# Generated by Django 2.1.7 on 2019-06-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0015_auto_20190613_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='course_subscriptions',
            field=models.ManyToManyField(blank=True, related_name='course_subscriptions', to='quiz.Course'),
        ),
    ]
