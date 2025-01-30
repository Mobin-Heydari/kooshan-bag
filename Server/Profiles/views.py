from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from Orders.models import Order
from Cart.cart import Cart
from Products.models import Category, PrimeryCategory
from ContactUs.models import Contact




class DashboardProfile(View):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            cart = Cart(request)
            contacts = Contact.objects.all()
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            return render(request, 'profiles/profile_dashboard.html', {
                'user' : user,
                'cart' : cart,
                'contacts' : contacts,
                'categories' : categories,
                'primery_categories' : primery_categories
            })
        else:
            return redirect('account:user_login')


class ProfileOrders(View):
    def get(self, request):
        if request.user.is_authenticated == True:
            user = request.user
            contacts = Contact.objects.all()
            user_orders = Order.objects.filter(user=user)
            cart = Cart(request)
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            return render(request, 'profiles/profile-orders.html', {
                'user' : user,
                'cart' : cart,
                'contacts' : contacts,
                'categories' : categories,
                'user_orders' : user_orders,
                'primery_categories' : primery_categories
            })

class ProfileOrderDetail(View):
    def get(self, request, pk):
        if request.user.is_authenticated == True:
            user = request.user
            cart = Cart(request)
            contacts = Contact.objects.all()
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            order = get_object_or_404(Order, id=pk, user=user)
            return render(request, 'profiles/order-detail.html', {
                'user' : user,
                'cart' : cart,
                'contacts' : contacts,
                'categories' : categories,
                'primery_categories' : primery_categories,
                'order' : order
            })