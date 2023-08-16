from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

PHASES = (
    ('SMT','SMT'),
    ('THT','THT'),
    ('tunning','tunning'),
    ('monitor assembly','monitor assembly'),
    ('communication config','communication config'),
    ('analysis','analysis'),
    ('correction','correction')
)


# class Items (models.Model):
#     item_code = models.CharField(max_length=50,primary_key=True)
#     name = models.CharField(max_length=100)
#     despription = models.TextField(max_length=100)

class Stock(models.Model):
    item_name = models.CharField(max_length=100,null=True)
    stock_in  = models.PositiveIntegerField(null=True)
    stock_out  = models.PositiveIntegerField(null=True)
    units = models.CharField(max_length=100,null=True)
    #editted here
    stock_in_date = models.DateField(default="2023-07-13", null=True)
    stock_out_date = models.DateField(auto_now=True)

class StockHistory(models.Model):
    Stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    item_name = models.CharField(null=True)
    stock_in = models.PositiveIntegerField(null=True)
    stock_out = models.PositiveIntegerField(null=True)
    stock_in_date = models.DateField(null=True)
    stock_out_date = models.DateField(null=True)
    history_date = models.DateTimeField(auto_now_add=True)

class Casing (models.Model):
    batch_number = models.CharField(max_length=100,null=True)
    device_name = models.CharField(max_length=100,null=True)
    quantity = models.PositiveIntegerField(null=True)
    date_start = models.DateField(auto_now=False,auto_now_add=False,)
    detail = models.CharField(max_length=1000,null=True)

class Production (models.Model):
    batch_number = models.CharField(max_length=100)
    phase = models.CharField(choices=PHASES,null=True)
    quantity_in = models.PositiveIntegerField(null=True)
    quantity_out = models.PositiveIntegerField(null=True)
    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(auto_now=True)
    detail = models.CharField(max_length=1000,null=True)

    def __str__(self):
        return str(self.date_end)


@receiver(post_save, sender=Stock)
def create_stock_history(sender, instance, **kwargs):
    StockHistory.objects.create(
        stock=instance,
        item_name=instance.item_name,
        stock_in=instance.stock_in,
        stock_out=instance.stock_out,
        stock_in_date=instance.stock_in_date,
        stock_out_date=instance.stock_out_date,
    )