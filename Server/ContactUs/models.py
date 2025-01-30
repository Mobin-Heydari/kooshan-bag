from django.db import models




class Contact(models.Model):
    phone = models.CharField(max_length=11,
                             verbose_name="شماره تلفن", null=True, blank=True)
    
    email = models.EmailField(verbose_name="ایمیل", null=True, blank=True)
    
    instagram_url = models.URLField(verbose_name="لینک بیج اینستا", null=True, blank=True)

    
    class Meta:
        verbose_name = "راه ارتباطی"
        verbose_name_plural = "راه های ارتباطی"
        
    
    def __str__(self):
        return self.phone
    
    
class UserContact(models.Model):
    name = models.CharField(max_length=200, 
                            verbose_name="نام کاربر")
    
    email = models.EmailField(verbose_name="ایمیل کاربر")
    
    phone = models.CharField(max_length=11,
                             verbose_name="شماره تماس کاربر")
     
    text = models.TextField(verbose_name="متن")
    
    
    
    class Meta:
        verbose_name = "پیام کاربر"
        verbose_name_plural = "پیام های کاربر"
        
        
        
    def __str__(self):
        return f'{self.name}---{self.phone}'