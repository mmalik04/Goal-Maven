# Generated by Django 3.2.19 on 2023-05-10 10:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20230510_0317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchevent',
            name='associated_player',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='associated_player', to='core.player'),
        ),
        migrations.AlterField(
            model_name='matchevent',
            name='pitch_area',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='core.pitchlocation'),
        ),
    ]
