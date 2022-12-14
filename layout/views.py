from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView,FormView,View, DeleteView
from django.contrib.auth.models import User
from datetime import date, timedelta
from .models import Contract, Order, Product, OrderProduct, Contractor, QuantifiedProduct
from .forms import ProductForm, ContractForm
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
    def post(self, *args, **kwargs):
        products = Product.objects.filter()
        for product in products:
            if self.request.POST.get("myButton"+str(product.name)):
                name = product.name
                return redirect('/order/create/?name=' + name)

class ProductCreateView(CompanyAndLoginRequiredMixin, FormView):
    form_class = ProductForm
    template_name = 'layout/product_form.html'
    success_url = "/products/"
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        messages.success(self.request, "You've created a new Product")
        return super().form_valid(form)

class ContractListView(CompanyAndLoginRequiredMixin, ListView):
    model = Contract
    template_name = 'layout/contract_list.html'
    context_object_name = 'contracts'
    def get_queryset(self):
        queryset = Contract.objects.filter(author__profile__company = self.request.user.profile.company)
        return queryset
    def post(self, *args, **kwargs):
        try:
            ID_contract, ID_product, order_product_quantity = self.get_IDs_and_quantity()
            quantified_product = self.get_quantified_product(ID_product)
            quantified_product.changeQuantity(-int(order_product_quantity))
            OrderProduct.objects.create(
                user = self.request.user, 
                contract= self.get_contract(ID_contract), 
                product = quantified_product.product, 
                quantity = order_product_quantity)
        except:
            messages.warning(self.request, "You can't order more products than currenty in contract")
        return redirect('contracts-list')

    def get_IDs_and_quantity(self):
        ID_cart_list = self.request.POST.getlist('cart')
        ID_cart_list = ID_cart_list[0].split("&")
        ID_contract= ID_cart_list[0]
        ID_product = ID_cart_list [1]
        object_quantity = self.request.POST.get(f"quantity{ID_contract}&{ID_product}")
        return ID_contract, ID_product, object_quantity
    def get_contract(self, ID_contract):
        return Contract.objects.filter(id = ID_contract).first()
    def get_quantified_product(self, ID_product):
        return QuantifiedProduct.objects.filter(id = ID_product).first()

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
        objects =  Contract.objects.filter(user_responsible=user).filter(
            type='PUBLIC_AUCTION').filter(
                end_date__lte=date.today()+timedelta(days=180)).filter(
                    end_date__gte=date.today())
        for object in objects:
            object.sendMailIfContractEnding()
        return objects

class ContractCreateView(CompanyAndLoginRequiredMixin, FormView):
    form_class = ContractForm
    template_name = 'layout/order_form.html'
    success_url = "/contracts/"
    def get_form_kwargs(self):
        kwargs = super(ContractCreateView, self).get_form_kwargs()
        kwargs['user'] = self.request.user 
        return kwargs 
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        items = form.cleaned_data['products']
        created = Contract.objects.last()
        for item in items:
            created_product = QuantifiedProduct.objects.create(product = item, number_of_product = 1)
            created.products.add(created_product)
            created.save()
        messages.success(self.request,"You've created new Contract")
        return super().form_valid(form)

class ContractorCreateView(CompanyAndLoginRequiredMixin, CreateView):
    model = Contractor
    fields = [
        'name',
        'email'
    ]
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request,"You've created new Contractor")
        return super().form_valid(form)

class OrderCreateView(CompanyAndLoginRequiredMixin, CreateView):
    model = Order
    fields = [
        'contract',
        'ordered_products',
        'date_of_order']
    def get_form_class(self):
        modelform = super().get_form_class()
        product_name = self.request.GET.get('name')
        if product_name is not None:
            modelform.base_fields['contract'].queryset = Contract.objects.filter(
                author__profile__company = self.request.user.profile.company).filter(
                products__product__name = product_name)
        else:
            modelform.base_fields['contract'].queryset = Contract.objects.filter(
                author__profile__company = self.request.user.profile.company)
        return modelform
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OrderCartView(View):
    def get(self, *args, **kwargs):
        order = OrderProduct.objects.filter(user=self.request.user)
        if order:
            context = {
                'object': order
            }
            return render(self.request, 'layout/order_cart.html', context)
        else:
            messages.warning(self.request, "You do not have an active order")
            return redirect("contracts-list")
    def post(self, *args, **kwargs):
        action, order_product_ID = self.get_action_and_order_product_ID()
        order_product = OrderProduct.objects.filter(id=order_product_ID).first()
        contact_to_change_quantity = Contract.objects.filter(id = order_product.contract.id).first()
        contract_products_to_change_quantity = contact_to_change_quantity.products.all()
        if action == 'minus':
            if order_product.quantity >1:
                order_product.quantity = order_product.quantity -1
                order_product.save()
                for product in contract_products_to_change_quantity:
                    if product.product == order_product.product:
                        product.changeQuantity(1)
            else:
                messages.warning(self.request, "You can't order 0 or less, delete order")
        if action == 'plus':
            for product in contract_products_to_change_quantity:
                if product.product == order_product.product:
                    try:
                        product.changeQuantity(-1)
                        order_product.quantity = order_product.quantity+1
                        order_product.save()
                    except:
                        messages.warning(self.request, "No more items in contract!")
        if action == 'delete':
            for product in contract_products_to_change_quantity:
                if product.product == order_product.product:
                    product.changeQuantity(order_product.quantity)
            order_product.delete()
        return redirect('order-cart')
    def get_action_and_order_product_ID(self):
        action_and_ID = self.request.POST.get('cart')
        action_and_ID = action_and_ID.split("&")
        action = action_and_ID[0]
        order_product_ID = int(action_and_ID[1])
        return action, order_product_ID

class ProductDetailView(CompanyAndLoginRequiredMixin, DetailView):
    model = Product
    context_object_name = 'product'

class ProductDeleteView(CompanyAndLoginRequiredMixin, DeleteView):
    model = Product
    success_url ="/" 
    template_name = "layout/object_delete.html"

class OrderDeleteView(CompanyAndLoginRequiredMixin, DeleteView):
    model = Order
    success_url ="/" 
    template_name = "layout/object_delete.html"

class ContractDeleteView(CompanyAndLoginRequiredMixin, DeleteView):
    model = Contract
    success_url ="/" 
    template_name = "layout/object_delete.html"