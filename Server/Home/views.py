from django.shortcuts import render
from django.views.generic import View
from Products.models  import PrimeryCategory, Category, Product
from Cart.cart import Cart
from ContactUs.models import Contact




class Home(View):
    def get(self, request):
        contacts = Contact.objects.all()
        primery_categories = PrimeryCategory.objects.all()
        categories = Category.objects.all()
        cart = Cart(request)
        heighest_sales_products = Product.objects.filter(available=True).order_by('sales')
        new_products = Product.objects.filter(available=True).order_by('-created')
        return render(request, 'home/index.html', {
            'cart' : cart,
            'contacts' : contacts,
            'categories' : categories,
            'new_products' : new_products,
            'primery_categories' : primery_categories,
            'heighest_sales_products' : heighest_sales_products
        })