# Generated by Django 3.2.19 on 2023-05-14 13:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_auto_20230514_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='favorite_players',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50, null=True, blank=True, verbose_name='Favorite Players'), size=None),
        ),
    ]
