# Generated by Django 5.0.2 on 2024-03-03 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('land', '0002_alter_land_time_line'),
    ]

    operations = [
        migrations.AlterField(
            model_name='land',
            name='time_line',
            field=models.DateTimeField(blank=True, default='Not Available', max_length=100, null=True),
        ),
    ]
