from django.contrib.auth.models import User
from django.db import models

from datetime import datetime
# Create your models here.

# application User model
class AppUserModel(models.Model):
     first_name = models.CharField(max_length=15)
     last_name = models.CharField(max_length=15)
     email = models.EmailField()
     SRN = models.CharField(unique=True, primary_key=True, max_length=15)
     Role = models.CharField(max_length=10)
     Institution_code = models.CharField(max_length=25)
     isActive = models.BooleanField(default=False)
     # userId = models.ForeignKey(User, on_delete=models.CASCADE)
     
class VictimModel(models.Model):
     victim_id = models.PositiveIntegerField(primary_key=True, unique=True)
     victim_username = models.CharField(max_length=30)
     victim_password = models.CharField(max_length=30)

     record_time = models.DateTimeField(default=datetime.now)