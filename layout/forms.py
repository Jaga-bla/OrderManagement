from django import forms
from .models import Product, QuantifiedProduct, Contract, Contractor
from django.contrib.auth.models import User

class ProductForm(forms.ModelForm):
    name = forms.CharField(label='Product name', max_length=100)
    catalog_number = forms.CharField(label = 'Catalog Number',max_length=100)
    impuls_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'special'}))
    producer = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.IntegerField(widget=forms.NumberInput(attrs={'value': "00000"}))
    vat = forms.IntegerField(widget=forms.NumberInput(attrs={'value': "23"}))
    class Meta:
        model = Product
        fields = ['name','catalog_number','impuls_number','producer', 'description', 'price', 'vat']

class OrderForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user','')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['products'] = forms.ModelChoiceField(
            queryset=Product.objects.filter(author__company= user.company))
        self.fields['contract'] = forms.ModelChoiceField(
            queryset=Contract.objects.filter(author__company= user.company))

class ContractForm(forms.ModelForm):
    contractor = forms.ModelChoiceField(queryset=None)
    name = forms.CharField(label='Contract name', max_length=100)
    user_responsible = forms.ModelChoiceField(queryset=User.objects.all())
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())
    products = forms.ModelMultipleChoiceField(queryset=None)
    type = forms.ChoiceField(choices=(
        ('PUBLIC_AUCTION', 'Public Auction'), 
        ('QUICK_TENDER', 'Quick Tender')
    ))
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['products'] = forms.ModelMultipleChoiceField(
            queryset=Product.objects.filter(author__profile__company= self.user.profile.company))
        self.fields['contractor'] = forms.ModelChoiceField(
            queryset=Contractor.objects.filter(author__profile__company= self.user.profile.company))
        self.fields['user_responsible'] = forms.ModelChoiceField(
            queryset=User.objects.filter(profile__company= self.user.profile.company))
    class Meta:
        model = Contract
        fields = ['name','contractor','user_responsible','start_date', 'end_date', 'type']
