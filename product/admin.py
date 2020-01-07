from django.contrib import admin
from .models import Customer, Vender, Products, Delivery, Order, Bill
# Register your models here.

admin.site.register(Customer)
admin.site.register(Vender)
admin.site.register(Products)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Bill)