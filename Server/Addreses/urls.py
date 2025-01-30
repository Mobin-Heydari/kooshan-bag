from django.urls import path
from . import views


app_name = "Addreses"


urlpatterns = [
    path('add-new-address/', views.UserAddAddres.as_view(), name="add_new_addres"),
    path('user-profile-addreses/', views.ProfileAddreses.as_view(), name="user_addreses"),
    path('delete-address/<int:pk>/', views.DeleteUserAddress.as_view(), name="delete_address"),
]
