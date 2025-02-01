from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from Products.models import Product, PrimeryCategory, Category
from Orders.models import Order
from Cart.cart import Cart
from ContactUs.models import Contact

from django.conf import settings
import requests
import json


#? sandbox merchant 
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"

description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8080/payment/zarinpal/verify/'


class PaymentView(View):
    def get(self, request, pk):
        if request.user.is_authenticated:
            contacts = Contact.objects.all()
            primery_categories = PrimeryCategory.objects.all()
            categories = Category.objects.all()
            cart = Cart(request)
            order = get_object_or_404(Order, id=pk)
            return render(request, 'payment/start-pay.html', {
                'order':order,
                'contacts' : contacts,
                'categories' : categories,
                'primery_categories' : primery_categories,
                'cart' : cart
            })
        else:
            return redirect('account:user_login')


class ZarinpalSendRequest(View):
    def get(self, request, pk):
        instance = get_object_or_404(
            Order,
            id = pk,
            user = request.user
        )
        request.session['order_id'] = str(instance.id)
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": instance.total_price,
        "Description": description,
        "email": instance.user.email,
        "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']), 'authority': response['Authority']}
                else:
                    return {'status': False, 'code': str(response['Status'])}
            return response
    
        except requests.exceptions.Timeout:
            return {'status': False, 'code': 'timeout'}
        except requests.exceptions.ConnectionError:
            return {'status': False, 'code': 'connection error'}
        return redirect('/')


class ZarinpalVerify(View):
    def get(self, request, authority):
        order_id = request.session['order_id']
        order = Order.objects.get(id=int(order_id))
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.total_price,
        "Authority": authority,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                order.paid = True
                order.order_code = str(response['RefID'])
                order.save()
                return render(request, 'payment/success.html', {'order':order, 'RefID':response['RefID']})
            else:
                return render(request, 'payment/failed.html', {'order':order})
        return response