from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Land(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    area_sqft = models.FloatField()
    description = models.TextField()
    photos = models.ImageField(upload_to='land_photos/', null=True, blank=True)
    video_tour = models.URLField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    reason_for_selling = models.TextField(null=True, blank=True)
    plot_number = models.CharField(max_length=100, null=True, blank=True)
    time_line = models.CharField(max_length=100, null=True, blank=True, default="Not Available") # desired timeline for closing sales

    def __str__(self):
        return self.location