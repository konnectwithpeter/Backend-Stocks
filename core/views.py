import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny 
from rest_framework.response import Response
from algo import a
from algo import algo
from core.models import Predictions, Stock, StockData
from core.serializers import PredictionSerializer, StockDataSerializer, Stockserializer


@api_view(['GET'])
@permission_classes([AllowAny])
def stocks_view(request):
    if request.method == 'GET':
        response = Stock.objects.all()
        serializer = Stockserializer(response, many=True)
        return Response(serializer.data) 

@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def stock_history_view(request):
    if request.method == 'POST':
        response = StockData.objects.filter(stock=request.data['stock'])
        print(request.data['stock'])        
        a.csv2json(request.data['stock'])
        serializer = StockDataSerializer(response, many=True)  
        return Response(serializer.data)
        #print(request)
    # Response() 
      
from datetime import date
  
@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def stock_prediction_view(request):
    if request.method == 'POST':
        #a.csv2json(request.data['stock'])        
        if Predictions.objects.filter(stock=request.data['stock']).exists():
            preds = Predictions.objects.get(stock=request.data['stock'])
            f1 = str(preds.timestamp-datetime.timedelta(days=0))
            f2 = date(int(f1[:4]), int(f1[5:7]), int(f1[8:11]))
            diff = date.today()-f2
            if(str(diff)=='0:00:00'):
                res = PredictionSerializer(preds)
                return Response(res.data)
            else:
                algo.prediction_algo(request.data['stock'])
                preds = Predictions.objects.get(stock=request.data['stock'])
                res = PredictionSerializer(preds)
                return Response(res.data)    
        else:
            algo.prediction_algo(request.data['stock'])
            preds = Predictions.objects.get(stock=request.data['stock'])
            res = PredictionSerializer(preds)
            return Response(res.data)
