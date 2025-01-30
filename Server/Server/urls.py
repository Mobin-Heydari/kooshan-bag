from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('products/', include('Products.urls', namespace="Products")),
    path('auth/', include('Accounts.urls', namespace="Accounts")),
    path('contacts/', include('ContactUs.urls', namespace="Contact")),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
