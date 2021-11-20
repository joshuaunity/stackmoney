from django.db import models
from django.contrib.auth.models import User, auth


# Create your models here.
class Transaction(models.Model):
    id = models.IntegerField(primary_key = True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30) 
    price = models.IntegerField(null=True) 
    phone = models.IntegerField(null=True) 
    ref = models.CharField(max_length=30) 
    address = models.CharField(max_length=30, null=True) 
    phone = models.IntegerField(default="0701234803") 
    ref = models.CharField(max_length=30, null=True) 
    address = models.CharField(max_length=30, default="123, Saint mark Street") 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name