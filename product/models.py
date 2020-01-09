from django.db import models

# Create your models here.

# class Admin(models.Model):
#     user_id = models.CharField(max_length=20)
#     Passwd = models.TextField(max_length=200)
#     binary = models.IntegerField(max_digits=1, null=False)



class Customer(models.Model):   #user
    c_name   = models.CharField(max_length=20)
    location = models.TextField(max_length=200)
    mobile   = models.IntegerField()
    def __str__(self):
        return self.c_name

class Vender(models.Model): #vendor
    v_name     = models.CharField(max_length=20)
    v_location = models.TextField(max_length=100)
    v_mobile   = models.IntegerField()
    def __str__(self):
        return self.v_name

class Products(models.Model):
    p_name   = models.CharField(max_length=20)
    p_type   = models.CharField(max_length=30)
    p_cost   = models.DecimalField(decimal_places=2, max_digits=200, null=False)
    p_count  = models.IntegerField()
    vender   = models.ManyToManyField(Vender)
    customer = models.ManyToManyField(Customer, blank = True) 
    def __str__(self):
        return self.p_name

class Order(models.Model):
    o_status  = models.TextField()
    # o_bill    = models.OneToOneField(Bill, on_delete = models.CASCADE, default= 0)
    o_vender  = models.ManyToManyField(Vender)
    o_user    = models.ManyToManyField(Customer)
    def __str__(self):
        return self.o_status

class Bill(models.Model):
    b_quantity  = models.IntegerField()
    b_amount    = models.DecimalField(decimal_places=2, max_digits=20, null=False)
    product     = models.ManyToManyField(Products)
    order      = models.OneToOneField(Order, on_delete = models.CASCADE, default= 0)
    def __str__(self):
        return "success"

class Delivery(models.Model):
    d_amount = models.DecimalField(decimal_places=2, max_digits=200, null=False)
    d_status = models.TextField(max_length=30)
    d_type = models.CharField(max_length=20)
    def __str__(self):
        return self.d_amount

class Cart(models.Model):
    user_id = models.TextField()
    sessions_id = models.TextField() #?
    c_product = models.ManyToManyField(Products, blank = True)
    c_quantity = models.IntegerField()
    #c_order = models.ForeignKey(Order, on_delete = models.CASCADE)
    c_order = models.OneToOneField(Order, on_delete = models.CASCADE,null = True)