from django import forms
from .models import Product, Order,Contract

class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Product name', max_length=100)
    catalog_number = forms.CharField(label = 'Catalog Number',max_length=100)
    impuls_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'special'}))
    producent = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.CharField(max_length=100)
    vat = forms.CharField(max_length=100)
    class Meta:
        model = Product
        fields = ['name','catalog_number','impuls_number','producent', 'description', 'price', 'vat']

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['products'] = forms.ModelChoiceField(
            queryset=Product.objects.filter(author__company= user.company))
        self.fields['contract'] = forms.ModelChoiceField(
            queryset=Contract.objects.filter(author__company= user.company))
    
