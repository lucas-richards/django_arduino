# Generated by Django 5.0.1 on 2024-01-30 02:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0002_production_input_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
