from django.db import models

class SearchCriteria(models.Model):
    location = models.CharField(max_length=100)
    min_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_price = models.DecimalField(max_digits=10, decimal_places=2)
    house_type = models.CharField(max_length=50, blank=True, null=True)
    land_plot_type = models.CharField(max_length=50, blank=True, null=True)
    # Add more fields as needed