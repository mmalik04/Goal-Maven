# Generated by Django 3.2.19 on 2023-05-10 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_player_jersy_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='career_start',
            field=models.DateField(default='2005-01-01'),
            preserve_default=False,
        ),
    ]
