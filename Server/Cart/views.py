from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import View
from Products.models import Product, PrimeryCategory, Category
from .cart import Cart
from ContactUs.models import Contact

# Create your views here.

class CartDetail(View):
    def get(self, request):
        if request.user.is_authenticated == True:
            contacts = Contact.objects.all()
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            cart = Cart(request)
            return render(request, 'cart/cart.html', {
                'cart' : cart,
                'contacts' : contacts,
                'categories' : categories,
                'primery_categories' : primery_categories
            })
        else:
            return redirect('account:user_login')

class CartAddView(View):
    def post(self, request, pk):
        if request.user.is_authenticated == True:
            product = get_object_or_404(Product, id=pk)
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            price = int(quantity) * int(product.price)
            cart = Cart(request)
            cart.add(product, color, price, int(quantity))
            return redirect('cart:cart_detail')
        else:
            return redirect('account:user_login')


class CartRemove(View):
    def get(self, request, unique_id):
        if request.user.is_authenticated == True:
            cart = Cart(request)
            cart.remove(unique_id)
            return redirect('cart:cart_detail')
        else:
            return redirect('account:user_login')
    

class ClearCart(View):
    def get(self, request):
        if request.user.is_authenticated == True:
            cart = Cart(request)
            cart.clear()
            return redirect('cart:cart_detail')
        else:
            return redirect('account:user_login')