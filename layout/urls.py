from django.urls import path
from . import views
from .views import (
    ProductListView, 
    ProductCreateView, 
    ContractCreateView, 
    ProductDetailView, 
    ContractListView, 
    OrderCreateView, 
    OrderUpdateView, 
    StorageCreateView,
    ContractorCreateView,
    ContractEndListView
)

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('', views.home, name = 'home'),
    path('products/', ProductListView.as_view(), name = 'products-list'),
    path('contracts/', ContractListView.as_view(), name = 'contracts-list'),
    path('contracts/end', ContractEndListView.as_view(), name = 'contracts-end'),
    path('orders/', views.OrderListView, name = 'orders-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('products/create/', ProductCreateView.as_view(), name = 'product-create'),
    path('contractor/create/', ContractorCreateView.as_view(), name = 'contractor-create'),
    path('storage/create/', StorageCreateView.as_view(), name = 'storage-create'),
    path('order/create/', OrderCreateView.as_view(), name = 'order-create'),
    path('order/<int:pk>/update/', OrderUpdateView.as_view(), name = 'order-update'),
    path('contracts/create/', ContractCreateView.as_view(), name = 'contract-create'),
]
