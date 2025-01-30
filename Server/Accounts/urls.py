from django.urls import path
from . import views



app_name = "account"


urlpatterns = [
    # Authentications & users
    path('user-login/', views.Userlogin.as_view(), name='user_login'),
    path('user-logout/', views.UserLogout.as_view(), name='user_logout'),
    path('user-register/', views.UserRegister.as_view(), name='user_register'),
]