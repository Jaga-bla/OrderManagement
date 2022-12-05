from django.urls import path
from . import views
from .views import (
    ProductCreateView, 
    ContractCreateView, 
    ProductDetailView, 
    ContractListView, 
    OrderCreateView,  
    StorageCreateView,
    ContractorCreateView,
    ContractEndListView
)

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('', views.home),
    path('products/', views.ProductListView, name = 'products-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('products/create/', ProductCreateView.as_view(), name = 'product-create'),
    path('contracts/', ContractListView.as_view(), name = 'contracts-list'),
    path('contracts/end', ContractEndListView.as_view(), name = 'contracts-end'),
    path('contracts/create/', ContractCreateView.as_view(), name = 'contract-create'),
    path('orders/', views.OrderListView, name = 'orders-list'),
    path('order/create/', OrderCreateView.as_view(), name = 'order-create'),
    path('contractor/create/', ContractorCreateView.as_view(), name = 'contractor-create'),
    path('storage/create/', StorageCreateView.as_view(), name = 'storage-create'),
]
