from django.urls import path
from . import views
from .views import ProductListView

urlpatterns = [
    path('home/', views.home, name= 'home'),
    path('', views.about),
    path('products/', ProductListView.as_view(), name = 'products-list'),
]
