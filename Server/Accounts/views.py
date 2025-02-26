from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from .models import User, OneTimePassword, ChangePasswordOTP
from Products.models import Category, PrimeryCategory

import uuid

from .forms import (
    LoginForm,
    RegisterForm,
    OtpForm,
    ResetPasswordForm,
    ChangePasswordForm
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

                        # Generate a random 6-digit code for the OTP
                        code = randint(100000, 999999)

                        token = uuid.uuid4()

                        # Create a new OneTimePassword instance with the generated code
                        otp = OneTimePassword.objects.create(
                            # Set the code for the OTP
                            code=code,
                            # Generate a UUID for the token
                            token=token,
                            email=cd['email'],
                            password=cd['password'],
                            f_name=cd['f_name'],
                            l_name=cd['l_name']
                        )

                        # Save the new OneTimePassword instance to the database
                        otp.save()

                        otp.get_expiration()  # Get the expiration time of the OTP

                        print(otp.code)
                                
                        return redirect(reverse('Accounts:check_otp') + f'?token={otp.token}')
                    else:
                        form.add_error('password', 'ایمل وارد شده قبلا استفاده شده')
                else:
                    form.add_error('password', 'رمز عبور باید بین ۸ تا ۱۶ کاراکتر باشد')
            else:
                form.add_error('password', 'رمز عبور خود را اشتباه وارد کردید')

        return render(request, 'account/register.html', {'form': form})


class CheckOtp(View):
    
    def get(self, request):
        
        if request.user.is_authenticated == False:
            form = OtpForm()
        
            return render(
                request, 'account/check_otp.html', {
                    'form' : form
                }
            )
        else:
            return redirect('home:home')
        
    
    def post(self, request):
        
        if request.user.is_authenticated == False:
            
            form = OtpForm(request.POST)

            token = request.GET.get('token')
            
            otp = get_object_or_404(OneTimePassword, token=token)
            
            if form.is_valid():
                
                cd = form.cleaned_data
                
                if int(cd['otp']) == int(otp.code):

                    otp.status_validation()

                    if otp.status == 'ACT':
                    
                        user = User.objects.create_user(
                            f_name = otp.f_name,
                            l_name = otp.l_name,
                            password = otp.password,
                            email = otp.email,
                        )
                        
                        user.save()
                        
                        otp.delete()
                        
                        login(request, user)
                        
                        return redirect('/')
                    else:
                        form.add_error('otp', 'کد احرازحویت شما منقضی شده است لطفا دوباره تلاش کنید!')
                else:
                    form.add_error('otp', 'کد وارد شده معتبر نیست!')
            else:
                form.add_error('otp', 'کد وارد شده معتبر نیست!')
        else:
            return redirect('/')
        return render(
            request, 'account/check_otp.html', {
                'form' : form,
            }
        )


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect('/')
    


class ResetPassword(View):

    def get(self, request):
        form = ResetPasswordForm()
        return render(request, 'account/reset_password.html', {'form': form})
        
    def post(self, request):
        form = ResetPasswordForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            
            email = cd['email']
    
            user_email_validation = User.objects.filter(email=email).exists()
            
            if user_email_validation:
                code = randint(100000, 999999)
                token = uuid.uuid4()
                
                otp = ChangePasswordOTP.objects.create(
                    email=email,
                    code=code,
                    token=token
                )
                otp.get_expiration()
                otp.save()
                print(code)
                return redirect(reverse('Accounts:validate_password_otp') + f'?token={token}')
            else:
                form.add_error('email', 'User with this email does not exist')
                return render(request, 'account/reset_password.html', {'form': form})
        else:
            return render(request, 'account/reset_password.html', {'form': form})



class ValidatePasswordOtp(View):
    
    def get(self, request):
        
        token = request.GET.get('token')
        form = OtpForm()
        
        try:
            otp = ChangePasswordOTP.objects.get(token=token)
            
            return render(request, 'account/check_otp.html', {'form': form})
        except otp.DoesNotExist:
            return redirect('Accounts:reset_password')
        
    
    def post(self, request):

        form = OtpForm(request.POST)
        
        token = request.GET.get('token')
        
        try:
            otp = ChangePasswordOTP.objects.get(token=token)
        except otp.DoesNotExist:
            return redirect('Accounts:reset_password')
        
        if form.is_valid():
            code = form.cleaned_data['otp']

            otp.status_validation()

            if int(code) == int(otp.code):
                if otp.status == 'ACT':
                    return redirect(reverse('Accounts:change_password')+ f'?token={token}')
                else:
                    form.add_error('otp', 'کد یکبار مصرف شما منقضی شده است!')
                    return render(request, 'account/check_otp.html', {'form': form})
            else:
                form.add_error('otp', 'کد وارد شده صحیح نیست!')
                return render(request, 'account/check_otp.html', {'form': form})
        else:
            return render(request, 'account/check_otp.html', {'form': form})
        


class ChangePassword(View):
    
    def get(self, request):
        
        form = ChangePasswordForm()
        
        return render(
            request, 'account/change_password.html', {
                'form' : form
            }
        )
        
    def post(self, request):
        
        form = ChangePasswordForm(request.POST)
        
        token = request.GET.get('token')
        
        password_otp = get_object_or_404(ChangePasswordOTP, token = token)
        
        if form.is_valid():
            
            cd = form.cleaned_data
            
            if len(cd['password_conf']) <= 8 and len(cd['password_conf']) >= 8:
            
                if cd['password'] == cd['password_conf']:
                    
                    user = User.objects.get(email=password_otp.email)
                
                    if user is not None:
                        
                        user.set_password(cd['password'])
                        
                        user.save()
                        
                        password_otp.delete()
                        
                        return redirect('home:home')
                    else:
                        return redirect('Accounts:reset_password')
                else:
                    form.add_error('password', 'پسورد های وارد شده باهم برابر نیستند!')
            else:
                form.add_error('password', 'اندازه رمزعبور باید بین 8 تا 16 کاراکتر باشد!')
        else:
            form.add_error('password', 'اطلاعات وارد شده معتبر نیستند!')
        return render(request, 'account/change_password.html', {'form': form})