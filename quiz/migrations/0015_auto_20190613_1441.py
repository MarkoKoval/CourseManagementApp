# Generated by Django 2.1.7 on 2019-06-13 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0014_auto_20190613_1349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
