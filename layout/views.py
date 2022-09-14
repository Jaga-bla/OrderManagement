from django.shortcuts import render, get_list_or_404
from django.views.generic import ListView, CreateView, DetailView
from .models import Contract, Product

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
        'number_in_contract']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
