from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import *


class Stockserializer(ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class StockDataSerializer(ModelSerializer):
    class Meta:
        model = StockData
        fields = '__all__'

class PredictionSerializer(ModelSerializer):
    class Meta:
        model = Predictions
        fields = '__all__'        
      