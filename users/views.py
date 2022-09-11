from django.shortcuts import render
from .forms import UserRegisterForm

def register(request):
    return render(request, 'users/register.html')

