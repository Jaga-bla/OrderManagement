from django import forms

class ProductForm(forms.Form):
    name = forms.CharField(label='Your name', max_length=100)
    catalog_number = forms.CharField(label = 'Catalog Number',max_length=100)
    impuls_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'special'}))
    producent = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.CharField(max_length=100)
    vat = forms.CharField(max_length=100)