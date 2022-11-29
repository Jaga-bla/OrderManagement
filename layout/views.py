from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contract, Order, Product, Storage, Contractor
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request,'layout/home.html')

@login_required
def ProductListView(response):
    products = Product.objects.all()
    if response.method == "POST":
        for product in products:
            if response.POST.get("myButton"+str(product.id)):
                print(response.POST)
                return redirect(reverse('order-create'))
    return render(response, "layout/product_list.html", {"products": products})

class ContractListView(LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contracts.html'
    context_object_name = 'contracts'

@login_required
def OrderListView(response):
    orders = Order.objects.all()
    if response.method == "POST":
        if response.POST.get("save"):
            print(response.POST)
            for order in orders:
                if response.POST.get("o"+str(order.id)) == "is-ordered":
                    order.is_ordered = True
                else: 
                    order.is_ordered = False
                order.save()
            for order in orders:
                if response.POST.get("d"+str(order.id)) == "is-delivered":
                    order.is_delivered = True
                else: 
                    order.is_delivered = False
                order.save()
    return render(response, "layout/order_list.html", {"orders": orders})

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
