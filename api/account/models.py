# Create your models here.
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from uuid import uuid4

class UserManager(BaseUserManager):
    def create_user(self, password, phone, first_name, last_name):       
        if not password:
            raise ValueError("User must have a password.")
        
        if not phone:
            raise ValueError("User must have a phone number.")
        
        if not first_name:
            raise ValueError("User must have a first name.")
        
        if not last_name:
            raise ValueError("User must have a last name.")

        user = self.model(
            phone = phone,
            first_name = first_name,
            last_name = last_name,
        )
        
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone, password):
        if not phone:
            raise ValueError("User must have an email address")
        
        if not password:
            raise ValueError("User must have a password.")

        user = self.model(
            phone = phone,
        )

        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save()

        return user

class User(AbstractBaseUser):
    uuid = models.UUIDField(default=uuid4, editable=False)
    
    phone = models.CharField(
        verbose_name='Phone Number',
        max_length=20,
        unique=True,
    )

    email = models.EmailField(
        verbose_name='Email',
        null=True,
        blank=True
    )

    password=models.CharField(
        max_length=124, 
        verbose_name='Password'
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    uuid = models.UUIDField(unique=True, editable=False, default=uuid4)

    #brolypmics
    is_available=models.BooleanField(default=True)

    EMAIL_FIELD = 'phone'
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    objects = UserManager()


    #Preferences

    #Cookies

    #Functnions
    def get_full_name(self):
        pass

    def get_short_name(self):
        pass

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
       return self.is_admin

    def has_perm(self, perm, obj=None):
       return self.is_admin

    def has_module_perms(self, app_label):
       return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

    def clean_password(self):
        password = self.password
        if not re.search('[A-Z]', password):
            raise ValidationError(_('The password must contain at least one uppercase letter.'), code='invalid_password')
        if not re.search('[!@#$%^&*]', password):
            raise ValidationError(_('The password must contain at least one special character.'), code='invalid_password')


    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.phone}"
    


