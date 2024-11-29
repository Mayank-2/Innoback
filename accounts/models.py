from django.db import models
import uuid
import os
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver


class UserManager(BaseUserManager):
    def create_user(self, email,  name, contact, password=None, password2=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            contact=contact

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, contact, name, password=None):
        user = self.create_user(
            email,
            password=password,
            name=name,
            contact=contact
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(
        verbose_name='Email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=200)
    contact = models.CharField(
        max_length=15, null=True, blank=True, default='')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'contact']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):

        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(max_length=225, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=225, blank=True, null=True)
    pin_code = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=225, blank=True, null=True)
    country = models.CharField(max_length=225, blank=True, null=True)

    def __str__(self):
        return self.user.name
    
    

