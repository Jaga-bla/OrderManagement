from django.db import models
from django.contrib.auth.models import User
from dateutil.relativedelta import relativedelta


class Contractor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    author = models.ForeignKey(User, on_delete = models.SET_NULL)
    def __str__(self):
        return self.name

class Contract(models.Model):
    name = models.CharField(max_length=100)
    contractor = models.ForeignKey(Contractor, on_delete=models.SET_NULL)
    start_date = models.DateField()
    end_date = models.DateField()
    author = models.ForeignKey(User, on_delete = models.SET_NULL)
    PUBLIC_AUCTION = 'PUBLIC_AUCTION'
    QUICK_TENDER = 'QUICK_TENDER'
    type_choises = [
        (PUBLIC_AUCTION, 'Public Auction'), 
        (QUICK_TENDER, 'Quick Tender')
    ]
    type = models.CharField(max_length=100, choices=type_choises)
    def is_ending(self):
        if self.end_date == date.today() + relativedelta(months = 6):
            return True
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    description = models.TextField()
    price = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete = models.SET_NULL)
    def __str__(self):
        return self.name

