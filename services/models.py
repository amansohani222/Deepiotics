from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=20, default=None)
    email = models.EmailField(max_length=50, primary_key=True)
    company_name = models.CharField(max_length=20)
    phone = models.IntegerField(max_length=13)
    hit = models.IntegerField(default=0)
    max_hit = models.IntegerField(default=5)
    key = models.CharField(max_length=50)

