# Generated by Django 3.2.19 on 2023-05-10 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_remove_stadium_nation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='jersy_number',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
