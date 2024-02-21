from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
from django.utils import timezone

# Create your models here.
class Equipment(models.Model):

    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    created_date = models.DateField(default=datetime.now)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return self.title

class Production(models.Model):

    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, null=True, blank=True)
    input_desc = models.CharField(max_length=100)
    # quantity number field
    quantity = models.IntegerField()
    # remove tiem zone
    created_at = models.DateTimeField(default=timezone.now)
    

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.input_desc
    
    
class Location(models.Model):
    qrcode = models.CharField(max_length=100)
    country_code = models.CharField(max_length=2)
    country_name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    postal = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    IPv4 = models.GenericIPAddressField(protocol='IPv4')
    state = models.CharField(max_length=255)
    created_date = models.DateField(default=datetime.now)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f'{self.city}, {self.state}, {self.country_name} ({self.country_code})'