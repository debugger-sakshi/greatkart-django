# Generated by Django 3.1 on 2021-11-21 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='ug',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default='slug', max_length=100, unique=True),
        ),
    ]
