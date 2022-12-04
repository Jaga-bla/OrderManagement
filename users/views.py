from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import UserRegisterForm, ProfileUpdateForm, UserUpdateForm, CompanyCreateForm
from django.contrib.auth.decorators import login_required
from django.views.generic import FormView, View
from django.contrib.auth.models import User

class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class UserRegisterView(GuestOnlyView,FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        request = self.request
        # # user = form.save(commit=False)
        # user.username = form.cleaned_data['username']
        # # user.save()
        # raw_password = form.cleaned_data['password1']
        # user = authenticate(username=user.username, password=raw_password)
        # login(request, user)
        if request.POST.get('new_company') == 'No':
            print(request.POST.get('new_company'))
            messages.success(request, ('You are successfully signed up! Now create your company.'))
            return redirect('login-company')
        if request.POST.get('new_company') == 'Yes':
            print(request.POST.get('new_company'))
            messages.success(request, ('You are successfully signed up! Now login to your company.'))
            return redirect('create-company')

def createCompanyView(request):
    user = request.user
    form = CompanyCreateForm
    context = {
        'user' : user,
        'form' : form
    }
    return render(request, 'users/create-company.html', context)

def loginCompanyView(request):
    user = request.user
    context = {
        user :'user'
    }
    return render(request, 'users/login-company.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        if profile_form.is_valid() and user_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm()
        profile_form = ProfileUpdateForm()
    user_info = User.objects.get(id = request.user.id)
    context = {
        'user_info' : user_info,
        'user_form' : user_form,
        'profile_form' : profile_form
    }
    return render(request, 'users/profile.html', context)