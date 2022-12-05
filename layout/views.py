from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView, UpdateView,FormView,View
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contract, Order, Product, Storage, Contractor
from .forms import ProductForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


def staff_required(login_url=None):
    return user_passes_test(lambda u: u.profile.company, login_url=login_url)

class CompanyRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.company:
            messages.info(request, "You Have to login or create company first!")
            return redirect('create-company')
        return super().dispatch(request, *args, **kwargs)

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

class ContractListView(CompanyRequiredMixin,LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contracts.html'
    context_object_name = 'contracts'

@login_required
def OrderListView(response):
    orders = Order.objects.all()
    if response.method == "POST":
        if response.POST.get("save"):
            for order in orders:
                if response.POST.get("o"+str(order.id)) == "is-ordered":
                    order.is_ordered = True
                else: 
                    order.is_ordered = False
                if response.POST.get("d"+str(order.id)) == "is-delivered":
                    order.is_delivered = True
                else: 
                    order.is_delivered = False
                order.save()
    return render(response, "layout/order_list.html", {"orders": orders})

class ContractEndListView(CompanyRequiredMixin,LoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contractend_list.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        user = User.objects.filter(username=self.request.user).first()
        return Contract.objects.filter(user_responsible=user).filter(
            type='PUBLIC_AUCTION').filter(end_date__lte=date.today()+timedelta(days=180))

class ContractCreateView(CompanyRequiredMixin,LoginRequiredMixin, CreateView):
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
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StorageCreateView(CompanyRequiredMixin,LoginRequiredMixin, CreateView):
    model = Storage
    fields = [
        'contract',
        'product',
        'number_of_products'
    ]

class ContractorCreateView(CompanyRequiredMixin,LoginRequiredMixin, CreateView):
    model = Contractor
    fields = [
        'name',
        'email'
    ]
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProductCreateView(CompanyRequiredMixin,LoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'layout/product_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OrderCreateView(CompanyRequiredMixin,LoginRequiredMixin, CreateView):
    model = Order
    fields = [
        'contract',
        'quantity',
        'date_of_order',
        'is_ordered', 
        'is_delivered',
        'date_of_order'
        ]
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProductDetailView(CompanyRequiredMixin,LoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
