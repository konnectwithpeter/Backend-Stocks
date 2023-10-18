from django.contrib import admin

from core.models import Predictions, Stock, StockData

# Register your models here.
class Stocks(admin.ModelAdmin):
    model = Stock
    list_display = ('stock', 'last_update', 'market_cap',)

admin.site.register(Stock, Stocks)    
admin.site.register(StockData)
admin.site.register(Predictions)