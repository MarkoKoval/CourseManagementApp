# Generated by Django 2.1.7 on 2019-06-21 11:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0021_auto_20190621_1332'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='lesson',
            unique_together={('name', 'course')},
        ),
    ]
