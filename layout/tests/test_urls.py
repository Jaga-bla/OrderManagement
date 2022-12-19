from django.test import SimpleTestCase
from django.urls import reverse, resolve
from layout import views
from layout.views import (
    ProductListView,
    ProductCreateView, 
    ContractCreateView, 
    ProductDetailView, 
    ContractListView, 
    OrderCreateView,  
    StorageCreateView,
    ContractorCreateView,
    ContractEndListView)

class TestUrls(SimpleTestCase):
    
    def test_products_list_url(self):
        url = reverse('products-list')
        self.assertEquals(resolve(url).func.view_class, ProductListView)

    # def test_product_detail_url(self):
    #     url = reverse('product-detail')
    #     self.assertEquals(resolve(url).func.view_class, ProductDetailView)
    
    def test_product_create_url(self):
        url = reverse('product-create')
        self.assertEquals(resolve(url).func.view_class, ProductCreateView)

    def test_contracts_list_url(self):
        url = reverse('contracts-list')
        self.assertEquals(resolve(url).func.view_class, ContractListView)

    def test_contracts_end_url(self):
        url = reverse('contracts-end')
        self.assertEquals(resolve(url).func.view_class, ContractEndListView)
    
    def test_contracts_create_url(self):
        url = reverse('contract-create')
        self.assertEquals(resolve(url).func.view_class, ContractCreateView)

    def test_orders_list_url(self):
        url = reverse('orders-list')
        self.assertEquals(resolve(url).func.view_class, views.OrderListView)

    def test_order_create_url(self):
        url = reverse('order-create')
        self.assertEquals(resolve(url).func.view_class, OrderCreateView)

    def test_contractor_create_url(self):
        url = reverse('contractor-create')
        self.assertEquals(resolve(url).func.view_class, ContractorCreateView)

    def test_storage_create_url(self):
        url = reverse('storage-create')
        self.assertEquals(resolve(url).func.view_class, StorageCreateView)