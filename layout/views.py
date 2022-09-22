from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Contract, Order, Product, Storage, Contractor
from django.contrib.auth.mixins import LoginRequiredMixin

def home(request):
    return render(request,'layout/home.html')


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'contracts.html'
    context_object_name = 'contracts'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    fields = [
        'name',
        'contractor',
        'start_date',
        'end_date',
        'products', 
        'type'
    ]

class StorageCreateView(LoginRequiredMixin, CreateView):
    model = Storage
    fields = [
        'contract',
        'product',
        'number_of_products'
    ]

class ContractorCreateView(LoginRequiredMixin, CreateView):
    model = Contractor
    fields = [
        'name',
        'email'
    ]

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = [
        'name',
        'catalog_number',
        'producent', 
        'description',
        'price',
        'vat']

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    fields = [
        'contract',
        'quantity',
        'date_of_order',
        'is_ordered', 
        'is_delivered',
        'date_of_order'
        ]


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    fields = [
        'is_ordered',
        'is_delivered'
    ]



class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
