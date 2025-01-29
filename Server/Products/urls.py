from django.urls import path
from . import views


app_name = "products"


urlpatterns = [
    path('detail/<slug:slug>/', views.ProductDetail.as_view(), name="product_detail"),
    path('', views.ProductListFilter.as_view(), name="products_list")
]