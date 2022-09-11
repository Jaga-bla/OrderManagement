from django.shortcuts import render

def logged_in(request):
    return render(request,'layout/home.html')

