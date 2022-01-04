from django.urls import include, path, reverse_lazy
from .views import Referal_view, request_payment
from django.contrib.auth import views as auth_views  # import this

app_name = 'Referview'
urlpatterns = [
    path('', Referal_view, name='referal'),
    path('request_commission/<int:pk>', request_payment, name='request_payment')
]
