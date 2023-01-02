from django.test import TestCase, Client
from django.urls import reverse
from users.models import Profile
from django.contrib.auth.models import User

class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.products_list = self.client.get(reverse('products-list'))
        # self.product_detail = self.client.get(reverse('product-detail'))
        self.product_create = self.client.get(reverse('product-create'))
        # self.contract_end = self.client.get(reverse('contracts-end'))
        # self.contracts_list = self.client.get(reverse('contracts-list'))
        self.orders_list = self.client.get(reverse('orders-list'))
        # self.order_create = self.client.get(reverse('order-create'))
        # self.contractor_create = self.client.get(reverse('contractor-create'))
        # self.storage_create = self.client.get(reverse('storage-create'))

    def test_ProductListView(self):
        self.assertEquals(self.products_list.status_code, 302)
        # self.assertTemplateUsed(self.products_list, 'layout/product_list.html')
    
    # # def test_ProductDetailView(self):
    # #     self.assertEquals(self.product_detail.status_code, 200)
    # #     self.assertTemplateUsed(self.product_detail, 'layout/product_detail.html')

    def test_ProductCreateView(self):
        self.assertEquals(self.product_create.status_code, 302)
        self.assertTemplateUsed(self.product_create , 'layout/product_create.html')

    # def test_ContractEndView(self):
    #     self.assertEquals(self.contract_end.status_code, 200)
    #     self.assertTemplateUsed(self.contract_end, 'layout/contractend-list.html')

    # def test_ContractsList(self):
    #     self.assertEquals(self.contracts_list.status_code, 200)
    #     self.assertTemplateUsed(self.contracts_list, 'layout/contracts.html')

    def test_OrdersListView(self):
        self.assertEquals(self.orders_list.status_code, 302)
        self.assertTemplateUsed(self.orders_list, 'layout/order_list.html')
    
    # def test_OrderCreateView(self):
    #     self.assertEquals(self.order_create.status_code, 200)
    #     self.assertTemplateUsed(self.order_create, 'layout/order_form.html')

    # def test_ContractorCreateView(self):
    #     self.assertEquals(self.contractor_create.status_code, 200)
    #     self.assertTemplateUsed(self.contractor_create, 'layout/contractor_form.html')
    
    # def test_StorageCreateView(self):
    #     self.assertEquals(self.storage_create.status_code, 200)
    #     self.assertTemplateUsed(self.storage_create, 'layout/storage_form.html')
    

