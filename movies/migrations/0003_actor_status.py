# Generated by Django 4.0.2 on 2022-02-22 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_raiting_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='actor',
            name='status',
            field=models.BooleanField(default=0, verbose_name='is_director'),
        ),
    ]
