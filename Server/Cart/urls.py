from django.urls import path
from . import views

app_name = "cart"



urlpatterns = [
    path('', views.CartDetail.as_view(), name="cart_detail"),
    path('add-to-cart/<int:pk>/', views.CartAddView.as_view(), name="add_to_cart"),
    path('item-remove/<str:unique_id>/', views.CartRemove.as_view(), name="item_remove"),
    path('clear-cart/', views.ClearCart.as_view(), name="clear_cart")
]
