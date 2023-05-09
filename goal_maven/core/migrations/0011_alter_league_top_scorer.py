# Generated by Django 3.2.19 on 2023-05-08 23:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_player_jersy_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='league',
            name='top_scorer',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='top_scorer', to='core.player'),
            preserve_default=False,
        ),
    ]
