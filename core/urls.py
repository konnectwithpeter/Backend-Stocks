from django.urls import path
from core.views import *

urlpatterns = [
    path("stocks/", stocks_view, name="stocks"),
    path("stock-history/", stock_history_view, name="stock-history"),
    path("stock-prediction/", stock_prediction_view, name="stock-predictions"),
]