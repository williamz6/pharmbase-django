from rest_framework import serializers
from backend.models import Drug, Order, OrderItem
from user.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= Profile
        fields= '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields= '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    orders=OrderSerializer(many=False)
    class Meta:
        model= OrderItem
        fields= '__all__'

class DrugSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drug
        fields = '__all__'