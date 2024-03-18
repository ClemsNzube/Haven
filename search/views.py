from rest_framework import generics
from rest_framework.response import Response
from .models import SearchCriteria
from .serializers import SearchCriteriaSerializer
from house.models import House
from land.models import Land

class SearchAPIView(generics.ListAPIView):
    serializer_class = SearchCriteriaSerializer

    def get_queryset(self):
        # Extract search parameters from request
        location = self.request.query_params.get('location')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        house_type = self.request.query_params.get('house_type')
        land_plot_type = self.request.query_params.get('land_plot_type')
        # Add more parameters as needed

        # Perform filtering based on search parameters
        houses = House.objects.filter(location__icontains=location, 
                                       price__gte=min_price, 
                                       price__lte=max_price,
                                       house_type=house_type)
        lands = Land.objects.filter(location__icontains=location, 
                                    price__gte=min_price, 
                                    price__lte=max_price,
                                    plot_type=land_plot_type)
        
        # You can further filter based on additional criteria here

        return houses, lands
