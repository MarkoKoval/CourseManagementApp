# Generated by Django 2.1.7 on 2019-06-14 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0016_user_course_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='description',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
