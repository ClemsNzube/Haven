from rest_framework import serializers
from .models import Land


class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'


class LandSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        exclude = ['is_available', 'owner']