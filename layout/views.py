from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Contract, Product

def home(request):
    return render(request,'layout/home.html')

def about(request):
    return render(request,'layout/about.html')

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

class ContractCreateView(CreateView):
    model = Contract
    fields = [
        'name',
        'contractor',
        'start_date',
        'end_date', 
        'author', 
        'type_choises'
    ]

class ProductCreateView(CreateView):
    model = Product
    fields = [
        'name',
        'contract',
        'catalog_number',
        'index_number', 
        'description', 
        'price',
        'vat',
        'number_in_contract',
        'author']

