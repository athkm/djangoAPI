 
from django.shortcuts import render
from rest_framework.views import APIView
from product.models import Products, Vender, Order, Bill, Delivery, Customer, Cart, VendorCostSet, OrderDetails
#from rest_framework import viewsets, permissions
# from .decorators import unauthenticated_user, allowed_users, admindecorator, userdecorator, vendordecorator, useradmindecorator
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer, CartSerializer, VendorCostSerializer
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import HttpResponse, JsonResponse
# from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly

import logging
logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py

from .forms import CreateUserForm


# @login_required(login_url='loginpage')
def home(request):
    count = User.objects.count()
    return render(request, 'home.html',{
        'count': count
    })

# @unauthenticated_user
def loginPage(request):
	# if request.user.is_authenticated:
	# 	return redirect('home')
	# else:
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'registration/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginpage')

def register(request):      #reload not loading new page....error msg stays even after reloading apge   
    if request.user.is_authenticated:
        return redirect('home')
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user +" Signin success")
            return redirect('login/')
    context = {'form':form}
    
    return render(request, 'registration/register.html', context)


def userPage(request):
    context = {}
    return render(request, 'user.html', context)

# @method_decorator( [useradmindecorator], name='dispatch')
class ProductViewset(APIView):
    #127.0.0.1:8000/products/id/
    
    def get(self, request):         #trying to access product that does not exist?
        if(request.GET.get('id')):
            product_id = request.GET.get('id')
            products = Products.objects.filter(pk = product_id)
            serialized=ProductSerializer(products, many=True).data
            # permission_classes = [IsAdminUser]
        else:
            products = Products.objects.all()
            serialized=ProductSerializer(products, many=True).data
        return JsonResponse({"products": serialized}, status=status.HTTP_200_OK)
  

#initial phase u need to make all vendors as vendor for this product
    def post(self, request):
        post_data = request.data
        productObj = Products(p_name=post_data["p_name"], p_type=post_data["p_type"], p_cost=post_data["p_cost"])#, p_count=post_data["p_count"],
        productObj.save()
        # for vender_ in post_data["vender"]:
        #     productObj.vender.add(vender_)
        for vender_ in Vender.objects.all():
            productObj.vender.add(vender_)  
        vendors = Vender.objects.all()
        for vendor_ in vendors:
            change_price = VendorCostSet()
            change_price.Changed_amount = post_data["p_cost"]
            change_price.product_key = productObj
            change_price.vendor_key = vendor_
            change_price.save()
        productObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)

    #after deleting, corresponding entries in vendor cost set also has to be deleted
    def delete(self, request):              #try and exception here?
        product_id = request.GET.get('id')
        print(product_id)
        Products.objects.filter(pk=product_id).delete()
        return Response({"status": "deleted"}, status.HTTP_200_OK)

    def put(self, request):     #updates name
        product_id = request.GET.get('id')
        post_data = request.data
        productObj = Products.objects.filter(pk=product_id)
        for product_ in productObj:    #any other way?
            product_.p_name = post_data["p_name"]
            product_.save(update_fields=["p_name"])
        return Response({"status": "updated"}, status.HTTP_200_OK)

# @method_decorator([userdecorator], name="dispatch")
class AddToCartViewset(APIView): #change to be done: create a cart automatically whean a customer is created
  
    def get(self, request):     #calculate product price in cart...sum_of_all(product_price*total_no)
        if(request.GET.get('id')):  
            cart_id = request.GET.get('id')
            carts = Cart.objects.filter(pk = cart_id)
            serialized=CartSerializer(carts, many=True).data
        else:
            cart = Cart.objects.all()
            serialized=CartSerializer(cart, many=True).data
        return JsonResponse({"cart": serialized}, status=status.HTTP_200_OK)
    
    #delete product from a cart. 127.0.0.1:8000/products/id/ (given product id must be in cart to delete)
    # @method_decorator([cartdecorator], name="dispatch")
    def delete(self, request):          #need to delete entry from orderdetailstable
        if(request.GET.get('id')): # pass id in param
            cart_id = request.GET.get('id')     
            if(request.GET.get('c_product')):#pass c_product id number in param 
                delete = int(request.GET.get('c_product'))
                if delete not in list(Cart.objects.filter(pk=cart_id).values_list("c_product", flat = True)):
                    return Response({"status": "Failure"}, status=status.HTTP_400_BAD_REQUEST)

            del_product = request.GET.get("c_product")
            product = Products.objects.get(pk = del_product)
            print(del_product)
            #print(del_product, request.GET.get('id'))
            carts = Cart.objects.filter(pk=cart_id)#.values_list("c_product", flat = True)
            carts1 = Cart.objects.get(pk = cart_id)
            carts1.c_quantity = carts1.c_quantity-1
            carts1.c_total = carts1.c_total - product.p_cost
            carts1.save()
            OrderDetails.objects.get(product_id = del_product, user_id = cart_id).delete()
            for cart_items in carts:
                cart_items.c_product.remove(del_product)
                cart_items.save()

                #print(i, del_product) 
            # print(carts1.c_product)
            serialized=CartSerializer(carts, many=True).data
        else:
            # cart = Cart.objects.all()
            # serialized=CartSerializer(cart, many=True).data
            # Cart.objects.all().delete()
            return Response({"status": "nothing to delete no id"}, status.HTTP_200_OK)
        return JsonResponse({"cart": serialized}, status=status.HTTP_200_OK)

    def put(self, request): #add a product to cart              # put...change to post?
        product_id = request.GET.get('id') #product id to be added in params
        product = Products.objects.get(pk=product_id)
        price = product.p_cost
        print(price)
        customer_id = request.GET.get("c_id") # customer id where it is to be added. cart and customer 1-1 relationship
        cart = Cart.objects.get(pk=customer_id)
        customer = Customer.objects.get(pk = customer_id)
        if product.cart_set.filter(pk=cart.pk).exists():
            return Response({"status": "product exists in cart"}, status.HTTP_400_BAD_REQUEST) # bad request?
        else:
            cart.c_quantity =cart.c_quantity+1
            cart.c_total = cart.c_total +  price
            cart.save()
            customer.cart.c_product.add(product_id)
            customer.save()
            check_order_details = OrderDetails.objects.filter(product_id = product_id, user_id = customer_id)
        # if(len(check_order_details) == 0):
            orderdetailsObj = OrderDetails()
            orderdetailsObj.product_id = Products.objects.get(pk = product_id)
            orderdetailsObj.user_id = Customer.objects.get(pk = customer_id)
            orderdetailsObj.quantity= 1
            orderdetailsObj.save()
        # customer = Customer.objects.filter(pk = customer_id)          ---> ?
        return Response({"status": "updated"}, status.HTTP_200_OK)

# @method_decorator([vendordecorator], name="dispatch")
class VendorViewset(APIView):
    def post(self, request):
        post_data = request.data
        venderObj = Vender(v_name = post_data["v_name"], v_location = post_data["v_location"], v_mobile = post_data["v_mobile"])
        venderObj.save()
        products = Products.objects.all()
        for i in products:
            change_price = VendorCostSet()
            change_price.Changed_amount = i.p_cost
            change_price.product_key = i
            change_price.vendor_key = venderObj
            change_price.save()
        # for i in products:
        #     print(i.id)
        
        # for vender_ in post_data["c_product"]:
        #     cartObj.c_product.add(product_)  
        #     cartObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)


    def get(self, request): #does not give the list of vendors. This is for vendoorcostset
        if(request.GET.get('id') and request.GET.get('p_id') ):
            vendor_id = request.GET.get('id')
            product_id = request.GET.get('p_id')
            vendors = VendorCostSet.objects.filter(pk = vendor_id, product_key = product_id)
            print(vendors)
            serialized=VendorCostSerializer(vendors, many=True).data
        else:
            vendors = VendorCostSet.objects.all()
            #print(vendors)
            serialized=VendorCostSerializer(vendors, many=True).data
        return JsonResponse({"vendors": serialized}, status=status.HTTP_200_OK)


    def put(self, request): #to reset the price
        new_amount = 120
        post_data = request.data
        vendor_id = request.GET.get('v_id')
        product_id = request.GET.get('p_id')
        entries = VendorCostSet.objects.get(vendor_key = vendor_id, product_key = product_id)
        entries.Changed_amount = new_amount
        entries.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)

#need to clear the cart once ordered --------------------------*-------------------------------------
class OrderViewSet(APIView):
  
    # @method_decorator([useradmindecorator], name='dispatch')
    def get(self, request):
        user_id = request.GET.get('u_id')
        user = Customer.objects.get(pk = user_id)
        order = Order.objects.get(pk = user_id)
        return Response({"status":order.o_status}, status.HTTP_200_OK)

    # @method_decorator([admindecorator], name='dispatch')
    def put(self, request):             #need to add try and except herre
        status = {
        0 : "Order Recieved",
        1 : "Shipped",
        2 : "Out for delivery",
        3: "Delievered"
        }
        status_key = list(status.keys())
        status_value = list(status.values())
        user_id = request.GET.get('u_id')
        user = Customer.objects.get(pk = user_id)
        order = Order.objects.get(pk = user_id)
        order.o_status = status_value[status_key[status_value.index(order.o_status)] + 1]   #try and except block here. IF Delievered dont do this operation
        order.save()
        return Response({"status":order.o_status})

    # @method_decorator([userdecorator], name="dispatch")
    def post(self, request): #check if order is placed for that id, if not create new order, else change status
        user_id = request.GET.get('u_id')
        cart = Cart.objects.get(pk = user_id)
        user = Customer.objects.get(pk = user_id)
        if(cart.c_total == None):
            return Response({"status":"Failure"}, status.HTTP_400_BAD_REQUEST) #use try exception return some status
        order = Order()
        products_list = list()      #make this dict with key_> prod name, value-> count of prod
        order.o_status = "Order Recieved"
        order.o_user = user  #once delivered remove this
        order.c_cart = cart     #how to return 
        for product_ in cart.c_product.all():
            #l =   product_.p_name + ", " + l        #for now string concat
            products_list.append(product_.p_name)
        order.save()

        #need to delete the cart items -> because order is complete
        responseData = {
            'id': order.id,
            'user_name': Customer.objects.get(pk = user_id).c_name,
            'order_status': order.o_status,
            'products': products_list,
            'amount': cart.c_total
        }   #calculate product price in cart...sum_of_all(product_price*total_no)
        return Response(responseData, status.HTTP_200_OK)
        # return Response({"status":"Success"}, status.HTTP_200_OK)
    
    # @method_decorator([userdecorator], name="dispatch")
    def delete(self, request):      
        pass

class BillViewSet(APIView):     #after customer api
    def get(self, request):
        customer_id = request.GET.get("c_id")
        customer = OrderDetails.objects.get(pk = customer_id)
        cart = Cart.objects.get(pk = customer_id)
        #cust_details = customer.cart.c_product.all()
        #print(customer)
        #print(cust_details[1])
        #print(customer.cart.c_total)
        # bill = Bill()
        # bill.b_quantity = 10 #hardcoding for nwo
        # bill.b_amount = customer.cart.c_total
        # for product_ in customer.products:
        #     print(product_)
        return Response({"status":"Success"}, status.HTTP_200_OK )        # return name, address, vendor name, vendor number, total amount,date
    

    #def delete(APIView):
# @method_decorator([userdecorator], name='dispatch')
class UpdateCart(APIView):
    def put(self, request):         #check if requested number of products are available. request < than count of product   
        product_id = request.GET.get('id')
        customer_id = request.GET.get("c_id")
        orderdetailsObj = OrderDetails.objects.get(user_id = customer_id, product_id = product_id)
        orderdetailsObj.quantity = orderdetailsObj.quantity + 1
        orderdetailsObj.save()
        return Response({"status": "updated"}, status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.GET.get('id')
        customer_id = request.GET.get("c_id")
        orderdetailsObj = OrderDetails.objects.get(user_id = customer_id, product_id = product_id)
        if(orderdetailsObj.quantity == 1):      #need to add code part where entry will be deleted from the cart 
            return Response({"status": "last item, delete the product from cart"}, status.HTTP_200_OK)
            # https://stackoverflow.com/questions/11663945/calling-a-rest-api-from-django-view    -> call this for last item so product can be deleted?
        else:
            orderdetailsObj.quantity = orderdetailsObj.quantity - 1
        orderdetailsObj.save()
        return Response({"status": "updated"}, status.HTTP_200_OK)
 


'''
class BillViewSet(APIView):     #after customer api
    def get(self, request):
        customer_id = request.GET.get("c_id")
        customer = OrderDetails.objects.get(pk = customer_id)
        cart = Cart.objects.get(pk = customer_id)
        #cust_details = customer.cart.c_product.all()
        #print(customer)
        #print(cust_details[1])
        #print(customer.cart.c_total)
        # bill = Bill()
        # bill.b_quantity = 10 #hardcoding for nwo
        # bill.b_amount = customer.cart.c_total
        # for product_ in customer.products:
        #     print(product_)
        return Response({"status":"Success"}, status.HTTP_200_OK )        # return name, address, vendor name, vendor number, total amount,date
    

    #def delete(APIView):
# @method_decorator([userdecorator], name='dispatch')
class UpdateCart(APIView):
    def put(self, request):         #check if requested number of products are available. request < than count of product   
        product_id = request.GET.get('id')
        customer_id = request.GET.get("c_id")
        orderdetailsObj = OrderDetails.objects.get(user_id = customer_id, product_id = product_id)
        orderdetailsObj.quantity = orderdetailsObj.quantity + 1
        orderdetailsObj.save()
        return Response({"status": "updated"}, status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.GET.get('id')
        customer_id = request.GET.get("c_id")
        orderdetailsObj = OrderDetails.objects.get(user_id = customer_id, product_id = product_id)
        if(orderdetailsObj.quantity == 0):      #need to add code part where entry will be deleted from the cart 
            pass
        else:       
            orderdetailsObj.quantity = orderdetailsObj.quantity - 1
        orderdetailsObj.save()
        return Response({"status": "updated"}, status.HTTP_200_OK)
 
'''