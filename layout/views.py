from django.shortcuts import render
from django.views.generic import ListView
from .models import Product, Contractor, Contract

def home(request):
    return render(request,'layout/home.html')

def about(request):
    return render(request,'layout/about.html')

def ProductListView(ListView):
    model = Product
    template_name = 'products.html'


