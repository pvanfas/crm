from rest_framework import routers, serializers, viewsets
from customers.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','name','email','phone','address','phone']
