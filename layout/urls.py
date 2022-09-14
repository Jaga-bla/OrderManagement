from django.urls import path, include
from . import views
from .views import ProductListView, ProductCreateView, ContractCreateView, ProductDetailView, ContractListView

urlpatterns = [
    path('home/', views.home, name = 'home'),
    path('', views.about),
    path('products/', ProductListView.as_view(), name = 'products-list'),
    path('contracts/', ContractListView.as_view(), name = 'contract-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name = 'product-detail'),
    path('products/create/', ProductCreateView.as_view(), name = 'products-create'),
    path('contracts/create/', ContractCreateView.as_view(), name = 'contract-create'),
]
