from django.db import models

class Livestock(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    health_status = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    detailed_information = models.TextField()
    # Add more fields as needed

    def __str__(self):
        return self.name
