from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from .models import driverLocation
from Customer.models import shipJob,ProdDesc
from .serializers import locationSerializer,shipJobSerializer,ProdDescSerializer


class ListTodo(generics.ListCreateAPIView):
    queryset = driverLocation.objects.all()
    serializer_class = locationSerializer


class DetailTodo(generics.RetrieveUpdateDestroyAPIView):
    queryset = driverLocation.objects.all()
    serializer_class = locationSerializer