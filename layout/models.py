from time import timezone
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import date, timedelta
from django.core.mail import send_mail
from django.conf import settings

class Company(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100,default='0000')

class Contractor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('home')

class Product(models.Model):
    name = models.CharField(max_length=100)
    catalog_number = models.CharField(max_length=100, default='0000')
    impuls_number = models.CharField(max_length=100,default='0000')
    producer = models.CharField(max_length=100)
    description = models.TextField()
    price = models.CharField(max_length=100)
    vat = models.CharField(max_length=100,default='%')
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'pk' : self.pk})

class QuantifiedProduct(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    number_of_product = models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.number_of_product} of {self.product}"

class Contract(models.Model):
    name = models.CharField(max_length=100)
    contractor = models.ForeignKey(Contractor, null=True, on_delete=models.SET_NULL)
    user_responsible = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='user_reponsible')
    start_date = models.DateField()
    end_date = models.DateField()
    products = models.ManyToManyField(QuantifiedProduct)
    type_choises = (
        ('PUBLIC_AUCTION', 'Public Auction'), 
        ('QUICK_TENDER', 'Quick Tender')
    )
    type = models.CharField(max_length=100, choices=type_choises)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='author')
    email_sent = models.BooleanField(default = False)
    def get_absolute_url(self):
        return reverse('storage-create')
    def __str__(self):
        return self.name  
    def get_products(self):
        return [product for product in self.products.all()]
    def sendMailIfContractEnding(self):
        subject = "Your contract is ending"
        message = (f"We would like to inform you, that contract {self.name} will expire on {self.end_date}")
        if self.end_date <= date.today()+timedelta(days=180) and self.email_sent == False:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [self.user_responsible.email])
            self.email_sent = True
            self.save()

class OrderProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    contract = models.ForeignKey(Contract, on_delete = models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"         

class Order(models.Model):
    contract = models.ForeignKey(Contract, null=True, on_delete=models.SET_NULL)
    ordered_products = models.ManyToManyField(OrderProduct)
    date_of_order = models.DateField(default=timezone.now)
    is_ordered = models.BooleanField('Is ordered', default = False)
    is_delivered = models.BooleanField('Is Ordered', default = False)
    author = models.ForeignKey(User, null=True, on_delete = models.SET_NULL)
    def get_absolute_url(self):
        return reverse('orders-list')
    def save(self, *args, **kwargs):
        if self.is_ordered == True and self.is_delivered == False:
            for product in self.ordered_products:
                updated_product = Contract.objects.filter(
                    products = product).first()
                updated_product.number_of_product = updated_product.number_of_product - product.number_of_product
                updated_product.save()
        super().save(*args, **kwargs)