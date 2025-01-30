from django.urls import path
from . import views

app_name = "profiles"



urlpatterns = [
    # Profiles
    path('dashboard/', views.DashboardProfile.as_view(), name='profile_dashboard'),
    path('orders/', views.ProfileOrders.as_view(), name='profile_orders'),
    path("order/detail/<int:pk>/", views.ProfileOrderDetail.as_view(), name="order_detail")
]
