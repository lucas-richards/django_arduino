from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date

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
    created_at = models.DateTimeField(default=datetime.now)
    

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.input_desc