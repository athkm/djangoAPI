from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=200, null=False)
