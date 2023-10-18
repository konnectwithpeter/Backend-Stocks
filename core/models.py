from django_mysql.models import ListCharField
from django.db import models
from matplotlib import ticker
from django.db.models.signals import post_save



class Stock(models.Model):
    stock = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, default="stock", blank=True)
    last_update = models.DateTimeField(null=True, blank=True)
    market_cap = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.stock)

    class Meta:
        ordering = ["last_update"]
        verbose_name_plural = "Stocks"


class StockData(models.Model):
    stock = models.CharField(max_length=100)
    dates = models.JSONField(null=True, blank=True)
    prices = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.stock)

    class Meta:
        verbose_name_plural = "Stocks Data"         

def post_save_receiver(sender, instance, *args, **kwargs):
    StockData.objects.filter(stock=instance.stock).exclude(timestamp=instance.timestamp).delete()

post_save.connect(post_save_receiver, sender=StockData)


class Predictions(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    preds = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    from_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.stock)

    class Meta:
        verbose_name_plural = "Predictions"  

