# Generated by Django 3.2.19 on 2023-05-07 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_user_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Date of birth'),
        ),
    ]
