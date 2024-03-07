from rest_framework import serializers
from .models import RentHouse
from house.models import House


class RentHouseSerializer(serializers.ModelSerializer):
    house_id = serializers.IntegerField(required=True)

    class Meta:
        model = RentHouse
        fields = '__all__'
        read_only_fields = ['user']

    def validate_house_id(self, value):
        if not House.objects.filter(id=value).exists():
            raise serializers.ValidationError('House does not exist')
        return value