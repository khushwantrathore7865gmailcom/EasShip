from django.urls import path
from .views import loginUser

app_name = 'user'
urlpatterns = [
    path('', loginUser, name='Login')
]
