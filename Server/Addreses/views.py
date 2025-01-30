from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import View
from .models import UserAddres
from Products.models import Category, PrimeryCategory
from Cart.cart import Cart
from ContactUs.models import Contact


class UserAddAddres(View):
    def post(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            state, city, address, postal_code = request.POST.get('state'), request.POST.get('city'), request.POST.get('address'), request.POST.get('postal_code')
            f_name, l_name, phone = request.POST.get('f_name'), request.POST.get('l_name'), request.POST.get('phone')
            plak, unit, = request.POST.get('plak'), request.POST.get('unit')
            user_addres = UserAddres.objects.create(
                user = user,
                phone = phone,
                f_name = f_name,
                l_name = l_name,
                state = state,
                city = city,
                addres = address,
                plak = plak,
                unit = unit,
                postal_code = postal_code
            )
            user_addres.save()
            next_page = request.POST.get('next_page')
            if next_page:
                return redirect(next_page)
            else:
                return redirect('/')
        else:
            return redirect('account:user_login')


class ProfileAddreses(View):
    def get(self, request):
        # Check if the user dashboard is the same user that sent the request
        if request.user.is_authenticated == True:
            contacts = Contact.objects.all()
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            user = request.user
            user_addreses = UserAddres.objects.filter(user=user)
            cart = Cart(request)
            return render(request, 'addreses/user_addreses.html', {
                'user' : user,
                'categories' : categories,
                'user_addreses' : user_addreses,
                'primery_categories' : primery_categories,
                'contacts' : contacts,
                'cart' : cart
            })
        else:
            # Redirect to the login page if the user dashboard is not the same user
            return redirect('account:user_login')
        

class DeleteUserAddress(View):
    def get(self, request, pk):
        if request.user.is_authenticated == True:
            user_address = UserAddres.objects.get(id=pk)
            user = request.user
            if user_address.user != user:
                return HttpResponse("You don't have permission to delete this address")
            else:
                user_address.delete()
                return redirect('/')
        else:
            return redirect('account:user_login')