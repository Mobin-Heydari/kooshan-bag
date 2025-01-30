from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin



class UserManager(BaseUserManager):
    def create_user(self, email, f_name, l_name, password=None):
        user = self.model(
            email=self.normalize_email(email),
            f_name=f_name,
            l_name=l_name,
            password=password
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, f_name, l_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            f_name=f_name,
            l_name=l_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="ایمیل",
        max_length=255,
        unique=True,
    )
    
    f_name = models.CharField(verbose_name="نام",
                              max_length=200, null=True)
    l_name = models.CharField(verbose_name="نام خانوادگی",
                              max_length=200, null=True)
    
    is_active = models.BooleanField(default=True,
                                    verbose_name="فعال")
    
    is_admin = models.BooleanField(default=False,
                                   verbose_name="ادمین")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['f_name', 'l_name']
    
    
    class Meta:
        ordering = ['email']
        verbose_name = "کاربر"
        verbose_name_plural = "کاربر ها"
        

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
