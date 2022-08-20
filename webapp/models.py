from django.contrib.auth.models import User
from django.db import models

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
     