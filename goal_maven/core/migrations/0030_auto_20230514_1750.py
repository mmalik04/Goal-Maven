# Generated by Django 3.2.19 on 2023-05-14 12:50

import datetime
import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_auto_20230511_2343'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(1996, 1, 5), verbose_name='Date of birth'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='favorite_players',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True, null=True, verbose_name='Favorite Players'), default=['Cristiano Ronaldo'], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='favorite_team',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Favorite Teams'), default=['Real Madrid'], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(default='noobmaster69', max_length=50, verbose_name='Username'),
            preserve_default=False,
        ),
    ]
