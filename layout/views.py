from django.shortcuts import render

def home(request):
    return render(request,'layout/home.html')

def about(request):
    return render(request,'layout/about.html')

