from django.urls import path, include
from . import views
from .views import ProductListView, ProductCreateView, ContractCreateView

urlpatterns = [
    path('home/', views.home),
    path('', views.about),
    path('products/', ProductListView.as_view(), name = 'products-list'),
    path('products/create/', ProductCreateView.as_view(), name = 'products-create'),
    path('contracts/create/', ContractCreateView.as_view(), name = 'contract-create'),
]
