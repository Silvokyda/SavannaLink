# models.py

from django.db import models
from django.contrib.auth.models import User

class Livestock(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    health_status = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    detailed_information = models.TextField()

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/product_images/')  
    quantity = models.PositiveIntegerField(default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username}'s Cart - {self.product.name}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=255, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    position = models.CharField(max_length=255, blank=True, null=True)
    work_number = models.CharField(max_length=15, blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    work_address = models.TextField(blank=True, null=True)
    current_password = models.CharField(max_length=255, blank=True, null=True)
    new_password = models.CharField(max_length=255, blank=True, null=True)
    make_account_public = models.BooleanField(default=False)
