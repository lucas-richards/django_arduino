# Generated by Django 5.0.1 on 2024-02-21 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipments', '0007_qrcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qrcode', models.CharField(max_length=100)),
                ('country_code', models.CharField(max_length=2)),
                ('country_name', models.CharField(max_length=255)),
                ('city', models.CharField(max_length=255)),
                ('postal', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('IPv4', models.GenericIPAddressField(protocol='IPv4')),
                ('state', models.CharField(max_length=255)),
            ],
        ),
    ]
