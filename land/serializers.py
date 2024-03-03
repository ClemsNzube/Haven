from rest_framework import serializers
from .models import Land


class LandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'


class LandSellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Land
        fields = '__all__'
        read_only_fields = ['is_available', 'owner']

        def create(self, validated_data):
            # Set the owner of the land to the authenticated user
            validated_data['owner'] = self.context['request'].user
            return super().create(validated_data)
