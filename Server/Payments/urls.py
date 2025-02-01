from django.urls import path
from . import views


app_name = "payment"


urlpatterns = [
    path('<int:pk>/', views.PaymentView.as_view(), name="payment_view"),
    path('zarinpal/send/<int:pk>/', views.ZarinpalSendRequest.as_view(), name='zarinpal_send_request'),
    path('zarinpal/verify/', views.ZarinpalVerify.as_view(), name="zarinpal_verify")
]
