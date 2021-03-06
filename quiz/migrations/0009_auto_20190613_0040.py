# Generated by Django 2.1.7 on 2019-06-12 21:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0008_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='no name yet', max_length=64, unique=True)),
                ('course_creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.User')),
            ],
        ),
        migrations.CreateModel(
            name='SearchTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='no name yet', max_length=64, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='search_tags',
            field=models.ManyToManyField(blank=True, related_name='search_tags', to='quiz.SearchTags'),
        ),
    ]
