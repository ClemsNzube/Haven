from rest_framework import serializers
from .models import BuyLand
from land.models import Land
from house.models import House


class BuyLandSerializer(serializers.ModelSerializer):
    land_id = serializers.IntegerField(required=True)  # Add a field for the land ID

    class Meta:
        model = BuyLand
        fields = ['land_id', 'full_name', 'phone_number', 'email', 'message']  # Include land_id in the fields
        read_only_fields = ['user']

    def validate_land_id(self, value):
        # Validate if the provided land ID exists in the database and is available for sale
        try:
            land = Land.objects.get(id=value, is_available=True)
        except Land.DoesNotExist:
            raise serializers.ValidationError("Land not found or not available for sale")
        return value
    
class BuyHouseSerializer(serializers.ModelSerializer):
    house_id = serializers.IntegerField(required=True) 

    class Meta:
        model = BuyLand
        fields = ['house_id', 'full_name', 'phone_number', 'email', 'message']

    def validate_house_id(self, value):
        # Validate if the provided house ID exists in the database and is available for sale
        try:
            house = House.objects.get(id=value, is_available=True)
        except House.DoesNotExist:
            raise serializers.ValidationError("House not found or not available for sale")
        return value
