from django.db import models
from PatnerCompany.models import comp_drivers
# Create your models here.
class driverLocation(models.Model):
    driver = models.ForeignKey(comp_drivers,on_delete=models.CASCADE)
    location = models.CharField(max_length=30000)
    updated_on = models.DateTimeField(auto_now_add=True)