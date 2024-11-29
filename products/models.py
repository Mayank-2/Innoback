from django.db import models
import uuid
from django.utils.text import slugify
from accounts.models import User
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver
import os


class UpcomingProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poster = models.FileField(upload_to='product_main_images/',null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=255,null=True, blank=True)

    def __str__(self):
        return self.title
    
@receiver(post_delete, sender=UpcomingProduct)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.poster:
        if os.path.isfile(instance.poster.path):
            os.remove(instance.poster.path)
    


@receiver(pre_save, sender=UpcomingProduct)
def delete_old_profile_files(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = UpcomingProduct.objects.get(id=instance.id)
            
            if old_instance.poster != instance.poster:
                old_instance.poster.delete(False)
                if os.path.isfile(old_instance.poster.path):
                    os.remove(old_instance.poster.path)

        except:
            pass


class Category(models.Model):
    heading = models.CharField(max_length=500,null=True, blank=True)
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    main_image = models.ImageField(upload_to='product_main_images/',null=True, blank=True)
    slug = models.SlugField(editable=False, unique=True,
                            blank=True, null=True, max_length=500)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.name}-{self.price}")
        return super(Products, self).save(*args, **kwargs)
    
@receiver(post_delete, sender=Products)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.main_image:
        if os.path.isfile(instance.main_image.path):
            os.remove(instance.main_image.path)
    


@receiver(pre_save, sender=Products)
def delete_old_profile_files(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = Products.objects.get(id=instance.id)
            
            if old_instance.main_image != instance.main_image:
                old_instance.main_image.delete(False)
                if os.path.isfile(old_instance.main_image.path):
                    os.remove(old_instance.main_image.path)

        except:
            pass


class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')
    # Optional alt text for accessibility
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.product.name}"
    
@receiver(post_delete, sender=ProductImage)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    


@receiver(pre_save, sender=ProductImage)
def delete_old_profile_files(sender, instance, **kwargs):
    if instance.id:
        try:
            old_instance = ProductImage.objects.get(id=instance.id)
            
            if old_instance.image != instance.image:
                old_instance.image.delete(False)
                if os.path.isfile(old_instance.image.path):
                    os.remove(old_instance.image.path)

        except:
            pass


class Orders(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.IntegerField()
    status = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(editable=False, unique=True,
                            blank=True, null=True, max_length=500)

    def __str__(self):
        return self.customer.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.customer}-{self.id}")
        return super(Orders, self).save(*args, **kwargs)


class Order_items(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    slug = models.SlugField(editable=False, unique=True,
                            blank=True, null=True, max_length=500)

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(
                f"{self.product.name}-{self.order}")
        return super(Order_items, self).save(*args, **kwargs)
