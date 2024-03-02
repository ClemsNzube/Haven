from django.db import models
from accounts.models import CustomUser

class House(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assuming each house has an owner (user)
    address = models.CharField(max_length=255)
    bedrooms = models.IntegerField(blank=True)
    bathrooms = models.IntegerField(blank=True)
    size_sqft = models.IntegerField(blank=True)
    description = models.TextField()  # Description of the property
    lease_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Lease price set by owner
    availability_date = models.DateField(null=True, blank=True)  # Availability date
    amenities = models.TextField()  # Amenities checklist or descriptive text
    property_type = models.CharField(max_length=100)  # Property type (e.g., apartment, house, etc.)
    pet_policy = models.CharField(max_length=100, null=True, blank=True)  # Pet policy
    is_for_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    photos = models.ImageField(upload_to='house_photos/', null=True, blank=True)  # High-quality photos
    video_tour = models.URLField(null=True, blank=True)  # Optional video tour


    def __str__(self):
        return self.address


