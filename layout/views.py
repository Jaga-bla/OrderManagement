from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, DetailView,FormView,View
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contract, Order, Product, Storage, Contractor
from .forms import ProductForm
from django.contrib import messages

def home(request):
    return render(request,'layout/home.html')

class CompanyAndLoginRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You Have to login or create account first.")
            return redirect('login')
        elif not request.user.profile.company:
            messages.info(request, "You Have to login or create company first.")
            return redirect('create-company')
        return super().dispatch(request, *args, **kwargs)

class ProductListView(CompanyAndLoginRequiredMixin, ListView):
    model = Product
    template_name = 'layout/product_list.html'
    context_object_name = 'products'
    def get_queryset(self):
        queryset = Product.objects.filter(author__profile__company = self.request.user.profile.company)
        return queryset
    def post(self, request, *args, **kwargs):
        products = Product.objects.filter()
        for product in products:
            if self.request.POST.get("myButton"+str(product.id)):
                print(self.request.POST)
                return redirect(reverse('order-create'))

class ProductCreateView(CompanyAndLoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'layout/product_form.html'
    success_url = "/products/"
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class ContractListView(CompanyAndLoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contracts.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        queryset = Contract.objects.filter(author__profile__company = self.request.user.profile.company)
        return queryset

class OrderListView(CompanyAndLoginRequiredMixin, ListView):
    model = Order
    template_name = 'layout/order_list.html'
    context_object_name = 'orders'
    def get_queryset(self):
        queryset = Order.objects.filter(author__profile__company = self.request.user.profile.company)
        return queryset
    def post(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        ID_list_ordered = request.POST.getlist('is_ordered')
        ID_list_delivered = request.POST.getlist('is_delivered')
        queryset.update(is_ordered = False)
        queryset.update(is_delivered = False)
        for x in ID_list_ordered:
            Order.objects.filter(pk = int(x)).update(is_ordered = True)
        for x in ID_list_delivered:
            Order.objects.filter(pk = int(x)).update(is_delivered = True)
        return redirect('orders-list')
        

class ContractEndListView(CompanyAndLoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contractend_list.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        user = User.objects.filter(username=self.request.user).first()
        return Contract.objects.filter(user_responsible=user).filter(
            type='PUBLIC_AUCTION').filter(end_date__lte=date.today()+timedelta(days=180))

class ContractCreateView(CompanyAndLoginRequiredMixin, CreateView):
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
    def get_form_class(self):
        user_company = self.request.user.profile.company
        modelform = super().get_form_class()
        modelform.base_fields['products'].queryset = Product.objects.filter(author__profile__company = user_company)
        modelform.base_fields['contractor'].queryset = Contractor.objects.filter(author__profile__company = user_company)
        modelform.base_fields['user_responsible'].queryset = User.objects.filter(profile__company = user_company)        
        return modelform
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class StorageCreateView(CompanyAndLoginRequiredMixin, CreateView):
    model = Storage
    fields = [
        'contract',
        'product',
        'number_of_products'
    ]
    def get_form_class(self):
        user_company = self.request.user.profile.company
        modelform = super().get_form_class()
        modelform.base_fields['product'].queryset = Product.objects.filter(author__profile__company = user_company)
        modelform.base_fields['contract'].queryset = Contract.objects.filter(author__profile__company = user_company)
        return modelform

class ContractorCreateView(CompanyAndLoginRequiredMixin, CreateView):
    model = Contractor
    fields = [
        'name',
        'email'
    ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OrderCreateView(CompanyAndLoginRequiredMixin, CreateView):
    model = Order
    fields = [
        'contract',
        'quantity',
        'date_of_order',
        'is_ordered', 
        'is_delivered',
        'date_of_order'
        ]
    
    def get_form_class(self):
        modelform = super().get_form_class()
        modelform.base_fields['contract'].queryset = Contract.objects.filter(author__profile__company = self.request.user.profile.company)
        return modelform

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProductDetailView(CompanyAndLoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'
