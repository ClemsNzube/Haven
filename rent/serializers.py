from rest_framework import serializers
from .models import RentHouse


class RentHouseSerializer(serializers.ModelSerializer):

    class Meta:
        model = RentHouse
        fields = '__all__'