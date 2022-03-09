from django.contrib import admin
from .models import patnerComp, comp_drivers, comp_Bids, comp_PastWork, comp_PresentWork, comp_Transport, Comp_address, \
    Comp_profile,shipJob_Saved,Orders

# Register your models here.
admin.site.register(patnerComp)
admin.site.register(comp_drivers)
admin.site.register(comp_Transport)
admin.site.register(comp_PresentWork)
admin.site.register(comp_PastWork)
admin.site.register(comp_Bids)
admin.site.register(Comp_profile)
admin.site.register(Comp_address)
admin.site.register(shipJob_Saved)
admin.site.register(Orders)