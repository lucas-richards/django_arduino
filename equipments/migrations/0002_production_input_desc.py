# Generated by Django 5.0.1 on 2024-01-29 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='production',
            name='input_desc',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
