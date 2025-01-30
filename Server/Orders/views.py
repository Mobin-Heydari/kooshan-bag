from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import View
from Addreses.models import UserAddres
from Cart.cart import Cart
from Products.models import Category, PrimeryCategory
from ContactUs.models import Contact
from .models import OrderItem, Order



class CreateOrder(View):
    def get(self, request):
        if request.user.is_authenticated: 
            contacts = Contact.objects.all()
            cart = Cart(request)
            user = request.user  # Get the user object from the request
            user_addreses = UserAddres.objects.filter(user=user)
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            return render(request, 'orders/create-order.html',{
                'cart' : cart,
                'contacts' : contacts,
                'categories' : categories,
                'user_addreses' : user_addreses,
                'primery_categories' : primery_categories
            })
        else:
            return redirect('account:user_login')
    

    def post(self, request):
        if request.user.is_authenticated:
            user = request.user
            cart = Cart(request)
            address = request.POST.get('address')
            instance = get_object_or_404(UserAddres, id=address, user=user)
            order = Order.objects.create(
                user = user,
                f_name = instance.f_name,
                l_name = instance.l_name,
                phone = instance.phone,
                postal_code = instance.postal_code,
                state = instance.state,
                city = instance.city,
                address = instance.addres,
                plak = instance.plak,
                unit = instance.unit,
                total_price = cart.get_total_price(),
                paid = False
            )
            order.save()
            for item in cart:
                order_item = OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                    color=item['color']
                )
                order_item.save()
            cart.clear()
            return redirect('payment:payment_view', order.id)
        else:
            return redirect('account:user_login')
            