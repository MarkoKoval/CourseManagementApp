# Generated by Django 2.1.7 on 2019-06-21 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0020_auto_20190621_1246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]