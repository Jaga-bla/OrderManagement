from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView, CreateView, DetailView, UpdateView
from .models import Contract, Order, Product
from django.db.models import F

def home(request):
    return render(request,'layout/home.html')

def about(request):
    return render(request,'layout/about.html')

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'

class ContractListView(ListView):
    model = Contract
    template_name = 'contracts.html'
    context_object_name = 'contracts'

class OrderListView(ListView):
    model = Order
    template_name = 'orders.html'
    context_object_name = 'orders'

class ContractCreateView(CreateView):
    model = Contract
    fields = [
        'name',
        'contractor',
        'start_date',
        'end_date', 
        'author', 
        'type'
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
        'number_in_contract']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OrderCreateView(CreateView):
    model = Order
    fields = [
        'contract',
        'contractor',
        'product',
        'quantity', 
        'date_of_order', 
        'is_delivered',
        ]


class OrderUpdateView(UpdateView):
    model = Order
    fields = ['is_delivered']

    # def OrderComplete(self):
    #     if self.is_delivered == True:
    #         order = Order.objects.get(self)
    #         for order_product in order.product.all():
    #             order_product.number_in_contract -= order.quantity
    #             order_product.save()
    #         order.save()




class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
