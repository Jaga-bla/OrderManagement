from time import timezone
from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import Profile
from django.contrib.auth.models import User
from datetime import datetime, timedelta

class Contractor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('')

class Product(models.Model):
    name = models.CharField(max_length=100)
    catalog_number = models.CharField(max_length=100, default='0000')
    impuls_number = models.CharField(max_length=100,default='0000')
    producent = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)
    vat = models.CharField(max_length=100,default='%')
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk' : self.pk})

class Contract(models.Model):
    name = models.CharField(max_length=100)
    contractor = models.ForeignKey(Contractor, null=True, on_delete=models.SET_NULL)
    user_responsible = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    products = models.ManyToManyField(Product)
    PUBLIC_AUCTION = 'PUBLIC_AUCTION'
    QUICK_TENDER = 'QUICK_TENDER'
    type_choises = [
        (PUBLIC_AUCTION, 'Public Auction'), 
        (QUICK_TENDER, 'Quick Tender')
    ]
    type = models.CharField(max_length=100, choices=type_choises)
    def get_absolute_url(self):
        return reverse('storage-create')
    def __str__(self):
        return self.name  
    def display_products(self): #return list of products related to specific contract
        return [product for product in self.products.all()]
    def storage(self): #return stock status as a list, related to list od products
        list_of_products = self.display_products()
        storage_list = []
        for p in list_of_products:
            update = Storage.objects.filter(product=p.id).filter(contract=self).first()
            storage_list.append(update.number_of_products)
        return storage_list

class Storage(models.Model):
    contract = models.ForeignKey(Contract, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    number_of_products = models.PositiveIntegerField(default=1)
    def __str__(self):
        return (self.contract.name + ' - ' + self.product.name)
    def get_absolute_url(self):
        return reverse('contracts-list')

class Order(models.Model):
    contract = models.ForeignKey(Storage, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField()
    date_of_order = models.DateField(default=timezone.now)
    is_ordered = models.BooleanField()
    is_delivered = models.BooleanField()
    def get_absolute_url(self):
        return reverse('orders-list')
    def save(self, *args, **kwargs):
        if self.is_ordered == True and self.is_delivered == False:
            try:
                update = Storage.objects.filter(
                    contract = self.contract.contract.id).filter(product = self.contract.product.id).first()
                update.number_of_products = update.number_of_products - self.quantity
                update.save()
            except:
                return reverse('orders-list')
        super().save(*args, **kwargs)
