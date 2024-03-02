from rest_framework import serializers
from .models import House

class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'

class HouseLeaseSerializer(serializers.ModelSerializer):
    is_for_sale = serializers.HiddenField(default=False)
    class Meta:
        model = House
        exclude = ['sale_price', 'owner']
        read_only_field = ['is_for_sale']

    def create(self, validated_data):
        validated_data['is_for_sale'] = False  # Set is_for_sale to False for lease
        return super().create(validated_data)

class HouseSaleSerializer(serializers.ModelSerializer):
    is_for_sale = serializers.HiddenField(default=False)

    class Meta:
        model = House
        exclude = ['lease_price', 'owner']  
        read_only_field = ['is_for_sale']

    def create(self, validated_data):
        validated_data['is_for_sale'] = True  # Set is_for_sale to True for sale
        return super().create(validated_data)
