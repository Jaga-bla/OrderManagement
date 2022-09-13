from django.db import models
from layout.models import Product, Contract, Contractor

class Order(models.Model):
    contractor = models.ManyToManyField(Contractor, null=True, on_delete = models.SET_NULL)
    contract = models.ManyToManyField(Contract, null=True, on_delete = models.SET_NULL)
    product = models.ManyToManyField(Product, null=True, on_delete = models.SET_NULL)
    number_of_products = models.IntegerField()
    date_of_order = models.DateField()
    is_delivered = models.BooleanField()
    ordered_product_number = models.Index(fields = ['product'])
