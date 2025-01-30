from django.db import models
from Accounts.models import User
from Products.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name="user_orders",
        on_delete=models.CASCADE, verbose_name="کاربر"
    )
    
    f_name = models.CharField(
        max_length=50,
        verbose_name="نام"
    )
    
    l_name = models.CharField(
        max_length=50,
        verbose_name="نام خانوادگی"
    )
    
    phone = models.CharField(
        max_length=11,
        verbose_name="شماره تلفن", null=True
    )
    state = models.CharField(
        max_length=200,
        verbose_name="استان", null=True
    )
    
    city = models.CharField(
        max_length=200,
        verbose_name="شهر"
    )
    
    address = models.TextField(verbose_name="آدرس", null=True)
    
    plak = models.CharField(
        max_length=200,
        verbose_name="پلاک", null=True
    )
    
    postal_code = models.CharField(
        max_length=200,
        verbose_name="کد پستی", null=True
    )
    
    unit = models.CharField(
        max_length=200,
        verbose_name="واحد", null=True
    )
    
    paid = models.BooleanField(
        verbose_name="وضعیت پرداخت",
        default=False
    )

    created = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="ایجاد شده"
    )
    
    updated = models.DateTimeField(
        auto_now=True, 
        verbose_name="آبدیت شده"
    )
    
    total_price = models.BigIntegerField(verbose_name="قیمت")
    
    order_code = models.CharField(
        max_length=100,
        verbose_name="شماره پیگری سفارش", null=True
    )

    class Meta:
        verbose_name = "سفارش"
        verbose_name_plural = "سفارشات"
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created']),
        ]

    def __str__(self):
        return f'Order {self.id}'



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order',
        verbose_name="سفارش",
        on_delete=models.CASCADE
    )
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name="محصولات سفارش"
    )
    
    price = models.BigIntegerField(verbose_name="قیمت")
    
    quantity = models.PositiveIntegerField(default=1)
    
    color = models.CharField(
        max_length=200, 
        verbose_name="رنگ"
    )
    
    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity