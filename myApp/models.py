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

    def __str__(self):
        return self.name
