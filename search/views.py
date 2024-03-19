from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SearchCriteriaSerializer
from .models import SearchCriteria

class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Deserialize and validate the search parameters
        serializer = SearchCriteriaSerializer(data=request.GET)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Extract validated search parameters
        location = serializer.validated_data.get('location')
        price_min = serializer.validated_data.get('price_min')
        price_max = serializer.validated_data.get('price_max')
        house_type = serializer.validated_data.get('house_type')
        land_plot_type = serializer.validated_data.get('land_plot_type')

        # Perform search based on the extracted parameters
        queryset = SearchCriteria.objects.all()  
        if location:
            queryset = queryset.filter(location__icontains=location)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if house_type:
            queryset = queryset.filter(house_type=house_type)
        if land_plot_type:
            queryset = queryset.filter(land_plot_type=land_plot_type)

        # Serialize the queryset and return the response
        serializer = SearchCriteriaSerializer(queryset, many=True)  
        return Response(serializer.data, status=status.HTTP_200_OK)
