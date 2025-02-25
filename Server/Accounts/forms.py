from django.core import validators
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import User

class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["email", "f_name", "l_name"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["email", "password", "f_name", "l_name", "is_active", "is_admin"]



class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'ایمیل'
        }
    ))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'رمز عبور'
        }
    ))



class RegisterForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'ایمیل'
        }
    ))
    password = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'رمز عبور'
        }
    ))
    
    password_conf = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'تکرار رمز عبور'
        }
    ))
    
    f_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'نام'
        }
    ))
    
    l_name = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'نام خانوادگی'
        }
    ))

class OtpForm(forms.Form):
    
    otp = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'رمز عبور'
        }
    ))