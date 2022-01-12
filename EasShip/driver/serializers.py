from rest_framework import serializers
from .models import driverLocation
from Customer.models import shipJob,ProdDesc

class locationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'driver',
            'location',
            'updated_on'
        )
        model = driverLocation
class shipJobSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = shipJob

class ProdDescSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'value',
            'Weight_box',
            'length',
            'width',
            'height'
        )
        model = ProdDesc