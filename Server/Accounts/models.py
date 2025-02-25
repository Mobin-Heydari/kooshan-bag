from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

import uuid


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



class OneTimePassword(models.Model):
     # Enum for OTP status using Django's TextChoices
    class OtpStatus(models.TextChoices):
        EXPIRED = 'EXP', 'منقضی شده'  # Represents an expired OTP
        ACTIVE = 'ACT', 'فعال'         # Represents an active OTP

    
    # Field to store the status of the OTP (active or expired)
    status = models.CharField(
        verbose_name="وضعیت",
        max_length=3,
        choices=OtpStatus.choices,
        default=OtpStatus.ACTIVE  # Default status is active
    )

    # Field to store a unique token for the OTP
    token = models.UUIDField(max_length=250, unique=True, default=uuid.uuid4)
    
    code = models.CharField(max_length=6)  # Field to store the OTP code

     # Field to store the expiration time of the OTP
    expiration = models.DateTimeField(blank=True, null=True)
    
    # Field to store the creation time of the OTP record
    created = models.DateTimeField(auto_now_add=True)
    

    class Meta:
        verbose_name = 'رمز عبور یکبار مصرف'
        verbose_name_plural = 'رمز های عبور یکبار مصرف'
    

    # String representation of the OTP model
    def __str__(self):
        return f'{self.status}----{self.code}----{self.token}'
    
    # Method to calculate and set the expiration time of the OTP
    def get_expiration(self):
        created = self.created  # Get the creation time
        expiration = created + timezone.timedelta(minutes=2)  # Set expiration to 2 minutes after creation
        self.expiration = expiration  # Update the expiration field
        self.save()  # Save the changes to the database
        
    # Method to validate the status of the OTP based on its expiration
    def status_validation(self):
        if self.expiration <= timezone.now():  # Check if the OTP has expired
            self.status = 'EXP'  # Set status to expired
            return self.status
        else:
            return self.status  # Return the current status