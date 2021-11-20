from rest_framework import serializers
from .models import Transaction
from . import views 
# views.get_random_string(20)

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'user', 'name', 'price', 'ref', 'phone', 'address'
        )