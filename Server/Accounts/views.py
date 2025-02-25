from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, HttpResponse
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
        if not request.user.is_authenticated:
            form = LoginForm(request.POST)

            if form.is_valid():
                cd = form.cleaned_data

                print(cd['email'])
                print(cd['password'])
                
                user = authenticate(username=cd['email'], password=cd['password'])

                print(user)
                
                if user:
                    login(request, user)
                    return redirect('/')
                else:
                    form.add_error('email', 'ایمیل یا رمز عبور معتبر نیست')
            else:
                form.add_error('email', 'ایمیل یا رمز عبور معتبر نیست')
        else:
            return redirect('/')
        
        primery_categories = PrimeryCategory.objects.all()
        categories = Category.objects.all()
        return render(request, 'account/login.html', {
            'primery_categories' : primery_categories,
            'categories' : categories,
            'form' : form,
        })



class UserRegister(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            form = RegisterForm()
            return render(request, 'account/register.html', {
                'primery_categories': primery_categories,
                'categories': categories,
                'form': form,
            })

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['password_conf']:
                if 8 <= len(cd['password_conf']) <= 16:
                    if not User.objects.filter(email=cd['email']).exists():

                        user = User.objects.create(
                            email=cd['email'],
                            f_name=cd['f_name'],
                            l_name=cd['l_name']
                        ) 
                        user.set_password(cd['password'])
                        user.save()
                        login(request, user)
                        return redirect("/")
                    else:
                        form.add_error('password', 'ایمل وارد شده قبلا استفاده شده')
                else:
                    form.add_error('password', 'رمز عبور باید بین ۸ تا ۱۶ کاراکتر باشد')
            else:
                form.add_error('password', 'رمز عبور خود را اشتباه وارد کردید')

        return render(request, 'account/register.html', {'form': form})



class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')