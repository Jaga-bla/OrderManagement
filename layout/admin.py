from curses.ascii import controlnames
from django.contrib import admin
from .models import Contractor, Contract, Product, Order

admin.site.register(Contractor)

admin.site.register(Contract)

admin.site.register(Product)

admin.site.register(Order)