from django import forms



class AddresForm(forms.Form):
    phone = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'شماره موبایل '
        }
    ))
    
    email = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'ایمیل'
        }
    ))
    city = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'شهر'
        }
    ))
    
    plak = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'پلاک'
        }
    ))
    
    postal_code = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent p-4 text-left text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'کد پستی'
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