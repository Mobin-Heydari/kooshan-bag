from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('Products.urls', namespace="Products")),
    path('auth/', include('Accounts.urls', namespace="Accounts")),
    path('contacts/', include('ContactUs.urls', namespace="Contact")),
    path('cart/', include('Cart.urls', namespace="Cart")),
    path('addreses/', include('Addreses.urls', namespace="Addreses")),
    path('orders/', include('Orders.urls', namespace="Orders")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
