# Generated by Django 3.2.19 on 2023-05-07 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20230507_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, default='1996-01-05', verbose_name='Date of birth'),
            preserve_default=False,
        ),
    ]
