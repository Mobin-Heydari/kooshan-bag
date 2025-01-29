from django import forms




class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(
        attrs={
            'class' : 'main-scroll peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            "placeholder" : "متن دیدگاه",
            "rows":3,
            "id" : 'comment'

        }
    ))
    
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            'class' : 'peer w-full rounded-lg border-none bg-transparent px-4 py-3 text-quaternary-700 placeholder-transparent focus:outline-none focus:ring-0 dark:text-primary-light',
            'placeholder' : 'عنوان دیدگاه',
            'id' : 'title'
        }
    ))
