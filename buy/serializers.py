from rest_framework import serializers
from .models import BuyLand
from land.models import Land


class BuyLandSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BuyLand
        fields = '__all__'
        read_only_fields = ['user']
