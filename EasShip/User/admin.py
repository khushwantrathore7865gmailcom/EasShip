from django.contrib import admin
from .models import User_custom, Referral, Commission_request

# Register your models here.
admin.site.register(User_custom)
admin.site.register(Referral)
admin.site.register(Commission_request)
