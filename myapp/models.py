from django.db import models
from django.contrib.auth.models import User, auth


# Create your models here.
class Transaction(models.Model):
    id = models.IntegerField(primary_key = True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=30) 
    price = models.IntegerField() 
    ref = models.CharField(max_length=30) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name