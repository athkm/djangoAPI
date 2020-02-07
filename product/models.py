from django.db import models
from django.contrib.auth.models import AbstractUser

# class MyUser(AbstractUser):
#     is_student = models.BooleanField('student status', default=False)
#     is_teacher = models.BooleanField('teacher status', default=False)


class Vender(models.Model): #vendor
    v_name     = models.CharField(max_length=20)
    v_location = models.TextField(max_length=100)
    v_mobile   = models.IntegerField()
    def __str__(self):
        return self.v_name

    

class Products(models.Model):
    #p_image -> ?
    p_name   = models.CharField(max_length=20)
    p_type   = models.CharField(max_length=30)
    p_cost   = models.DecimalField(decimal_places=2, max_digits=200, null=False)
    vender   = models.ManyToManyField(Vender) #when last vendor of this product is deleted product is not deleted 
    def __str__(self):
        return self.p_name



class Customer(models.Model):   #user
    c_name   = models.CharField(max_length=20)
    location = models.TextField(max_length=200)
   # cart     = models.OneToOneField(Cart, on_delete = models.CASCADE)
    mobile   = models.IntegerField()
    #products = models.ManyToManyField(Products, blank = True) #can remove this? Onetoone with cart and cart has products
    def __str__(self):
        return self.c_name


class OrderDetails(models.Model):
    user_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    product_id = models.ForeignKey(Products, on_delete = models.PROTECT)
    #vendor_id = models.ForeignKey(Vender, on_delete = models.PROTECT)
    quantity = models.IntegerField()


#everytime u create a user, create a cart and link it to that user
class Cart(models.Model):
    #sessions_id = models.TextField() #?
    c_product = models.ManyToManyField(Products, blank = True)
    c_quantity = models.IntegerField(default = 0, blank=True)  #comment this ?
    #orderdetails    
    c_total = models.DecimalField(decimal_places=2, max_digits=200, default = 0, blank=True) #need to make null false and default s 0
    c_customer = models.OneToOneField(Customer, on_delete=models.CASCADE, primary_key = True)
    # def __str__(self):
    #     return str(type(self.c_product))




class Order(models.Model):
    o_status  = models.TextField()  # user and product
    #o_vender  = models.ManyToManyField(Vender) -> access from OrderDetails table
    o_user    = models.ForeignKey(Customer, on_delete = models.CASCADE)    #models.PROTECT?/
    c_cart = models.OneToOneField(Cart, on_delete = models.CASCADE,null = True) #many not one
    def __str__(self):
        return self.o_status

class Bill(models.Model):   #useless? can be obtained by the order table?
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

class VendorCostSet(models.Model):  #->API for this is remaining 
    Changed_amount  = models.DecimalField(decimal_places=2, max_digits=200, null=False)
    vendor_key = models.ForeignKey(Vender, on_delete = models.CASCADE, null = True)
    product_key = models.ForeignKey(Products, on_delete = models.CASCADE, null = True)


#S3 -> key-value