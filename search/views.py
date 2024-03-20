from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import SearchCriteria
from .serializers import SearchCriteriaSerializer, YourModelSerializer

class SearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        # Extract query parameters for location, price range, and house type
        location = request.GET.get('location')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        house_type = request.GET.get('house_type')

        # Filter queryset based on the provided parameters
        queryset = SearchCriteria.objects.all()  # Replace YourModel with your actual model

        if location:
            queryset = queryset.filter(location__icontains=location)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if house_type:
            queryset = queryset.filter(house_type__icontains=house_type)

        # Serialize the queryset and return the response
        serializer = SearchCriteriaSerializer(queryset, many=True)  # Replace YourModelSerializer with your actual serializer
        return Response(serializer.data, status=status.HTTP_200_OK)
