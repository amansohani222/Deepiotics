from django.contrib import admin

# Register your models here.
from services.models import Customer

admin.site.register(Customer)