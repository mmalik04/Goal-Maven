# Generated by Django 3.2.19 on 2023-05-18 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_playerrole_role_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerrole',
            name='role_key',
            field=models.CharField(max_length=3, unique=True),
        ),
    ]
