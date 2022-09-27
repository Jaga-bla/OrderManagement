from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from datetime import date, timedelta
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
    template_name = 'layout/contracts.html'
    context_object_name = 'contracts'

class OrderListView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

class ContractEndListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contractend_list.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        user = User.objects.filter(username=self.request.user).first()
        return Contract.objects.filter(user_responsible=user).filter(
            type='PUBLIC_AUCTION').filter(end_date__lte=date.today()+timedelta(days=180))


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    fields = [
        'name',
        'contractor',
        'start_date',
        'end_date',
        'products', 
        'type',
        'user_responsible'
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
