from django.contrib import admin
from .models import Customer, Vender, Products, Delivery, Order, Bill, Cart, VendorCostSet, OrderDetails
# Register your models here.

admin.site.register(Customer)
admin.site.register(OrderDetails)
admin.site.register(Vender)
admin.site.register(Products)
admin.site.register(Delivery)
admin.site.register(Order)
admin.site.register(Bill)
admin.site.register(Cart)
admin.site.register(VendorCostSet)