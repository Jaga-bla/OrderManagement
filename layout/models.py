from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.urls import reverse

class Contractor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    author = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    def __str__(self):
        return self.name

class Contract(models.Model):
    name = models.CharField(max_length=100)
    contractor = models.ForeignKey(Contractor, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    author = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    PUBLIC_AUCTION = 'PUBLIC_AUCTION'
    QUICK_TENDER = 'QUICK_TENDER'
    type_choises = [
        (PUBLIC_AUCTION, 'Public Auction'), 
        (QUICK_TENDER, 'Quick Tender')
    ]
    type = models.CharField(max_length=100, choices=type_choises)
    def list_of_products(self):
        return Product.objects.filter(contract=self)
    def is_ending(self):
        pass
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    catalog_number = models.CharField(max_length=100, default='0000')
    index_number = models.CharField(max_length=100,default='0000')
    description = models.TextField()
    price = models.CharField(max_length=100)
    vat = models.CharField(max_length=100,default='%')
    number_in_contract = models.IntegerField(default=1)
    author = models.ForeignKey(User,  null=True, on_delete = models.SET_NULL)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk' : self.pk})


