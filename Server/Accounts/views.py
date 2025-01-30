from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.views.generic import View
from .models import User
from Products.models import Category, PrimeryCategory


from .forms import (
    LoginForm,
    RegisterForm
)
from random import randint


class Userlogin(View):
    def get(self , request):
        if request.user.is_authenticated == True:
             return redirect('/')
        else:
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            form = LoginForm
            return render(request, 'account/login.html', {
                'primery_categories' : primery_categories,
                'categories' : categories,
                'form' : form,
            })
    
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['email'], password=cd['password'])
            if user is not None:
                login(request, user)
                return redirect("/")
        return render(request, 'account/login.html', {'form':form})


class UserRegister(View):
     def get(self, request):
        if request.user.is_authenticated == True:
            return redirect('/')
        else:
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            form = RegisterForm()
            return render(request, 'account/register.html', {
                'primery_categories' : primery_categories,
                'categories' : categories,
                'form' : form,
            })
     

     def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['password_conf']:
                if len(cd['password_conf']) <= 8 and len(cd['password_conf']) >= 8 :
                    user = User.objects.create(
                        email = cd['email'],
                        password = cd['password'],
                        f_name = cd['f_name'],
                        l_name = cd['l_name']
                    )
                    login(request, user)
                    return redirect("/")
                else:
                    form.add_error('password_conf', 'رمز عبور وارد شده کوچکتر از ۸ و یا بزرگتر از ۱۶ است')
            else:
                form.add_error('password_conf', 'رمز عبور خود را اشتباه وارد کردید')

        return render(request, 'account/register.html', {'form':form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')