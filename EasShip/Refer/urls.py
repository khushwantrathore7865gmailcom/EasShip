from django.urls import include, path, reverse_lazy
from .views import Referal_view
from django.contrib.auth import views as auth_views  # import this

app_name = 'Refer'
urlpatterns = [
    path('', Referal_view, name='referal'),
]
