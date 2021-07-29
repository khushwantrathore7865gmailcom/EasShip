from django.contrib import admin
from .models import customer, Customer_profile, Customer_address, shipJob, ProdDesc

# Register your models here.
admin.site.register(customer)
admin.site.register(Customer_profile)
admin.site.register(Customer_address)
admin.site.register(shipJob)
admin.site.register(ProdDesc)