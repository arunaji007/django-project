from django.db import models
from django.conf import settings


class Product(models.Model):
    class Meta:
        db_table = 'shop"."product'
        
    name = models.CharField(max_length=200)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.name


class Purchase(models.Model):

    class Meta:
        db_table = 'shop"."purchase'

    customer_email = models.EmailField()  # only customer identifier
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

class PurchaseItem(models.Model):
    
    class Meta:
        db_table = 'shop"."purchase_item'
        
    purchase = models.ForeignKey(Purchase, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price_with_tax = models.DecimalField(max_digits=10, decimal_places=2)


class Denomination(models.Model):
    class Meta:
        db_table = 'shop"."denomination'
        
    value = models.PositiveIntegerField(unique=True)


class DenominationCount(models.Model):
    class Meta:
        db_table = 'shop"."denomination_count'
        
    purchase = models.ForeignKey(Purchase, related_name="denomination_counts", on_delete=models.CASCADE)
    denomination = models.ForeignKey(Denomination, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()