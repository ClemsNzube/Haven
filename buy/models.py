from django.db import models
from accounts.models import CustomUser
from land.models import Land
from house.models import House

# Create your models here.
class BuyLand(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    land = models.ForeignKey(Land, on_delete=models.CASCADE, null=True)
    house = models.ForeignKey(House, on_delete=models.CASCADE, null=True)
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.full_name