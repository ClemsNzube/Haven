from rest_framework import serializers
from .models import BuyLand


class BuyLandSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyLand
        fields = '__all__'
