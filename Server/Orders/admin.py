from django.contrib import admin
from .models import Order, OrderItem




class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'f_name', 'l_name', 
                    'address', 'postal_code', 'city', 'paid',
                    'created', 'updated',]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
