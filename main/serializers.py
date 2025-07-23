from rest_framework import serializers
from main.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields= '__all__'


class ViewProductSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    foreign_currency = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields= '__all__'

    def get_price(self,obj):
        return f"${obj.price}"
    
    def get_foreign_currency(self,obj):
        Rs_price = round(obj.price * 80, 3)
        return f"₹{Rs_price}"


