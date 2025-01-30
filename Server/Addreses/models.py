from django.db import models
from Accounts.models import User



class UserAddres(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_addres", verbose_name="کاربر"
    )
    
    phone = models.CharField(
        max_length=200, 
        verbose_name="شماره تلقن"
    )
    
    f_name = models.CharField(
        max_length=200, 
        verbose_name="نلم"
    )
    
    l_name = models.CharField(
        max_length=200,
        verbose_name="نام خانوادگی"
    )
    
    state = models.CharField(
        max_length=200,
        verbose_name="استان"
    )
    
    city = models.CharField(
        max_length=200,
        verbose_name="شهر"
    )
    
    addres = models.TextField(verbose_name="آدرس")
    
    plak = models.CharField(
        max_length=200,
        verbose_name="پلاک"
    )
    
    unit = models.CharField(
        max_length=200,
        verbose_name="واحد"
    )
    
    postal_code = models.CharField(
        max_length=200, 
        verbose_name="کد پستی"
    )
    
    
    class Meta:
        verbose_name = "آدرس کاربر ها"
        verbose_name_plural = "آدرس های کاربر ها"