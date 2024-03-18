from rest_framework import serializers
from .models import SearchCriteria

class SearchCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchCriteria
        fields = '__all__'