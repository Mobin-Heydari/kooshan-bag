from django import forms
from django.core import validators



class UserContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
        'placeholder' : 'نام شما',
        'id' : 'name'
    }))
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class' : 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
        'placeholder' : 'ایمیل',
        'id' : 'email'
    }), validators=[validators.EmailValidator])
    
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
        'placeholder' : 'شماره تماس',
        'id' : 'number'
    }), validators=[validators.MaxLengthValidator(12)])
    
    text = forms.CharField(widget=forms.Textarea(attrs={
        'class' : 'main-scroll peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
        'placeholder' : 'پیام شما',
        'id' : 'message'
    }))