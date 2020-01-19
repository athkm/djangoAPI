from django.shortcuts import render
from rest_framework.views import APIView
from product.models import Products, Vender, Order, Bill, Delivery, Customer, Cart, VendorCostSet
#from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer, CartSerializer, VendorCostSerializer
from django.shortcuts import get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from rest_framework.permissions import IsAuthenticated

import logging
logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py

def home(request):
    count = User.objects.count()
    return render(request, 'home.html',{
        'count': count
    })


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {'message': 'Hello, World!'}
        return Response(content)
'''
after signing up in shell try
from django.contrib.auth.models import User     // user table?
User.objects.count()
u = User.objects.first()
u.username
'''

def signup(request):
    if(request.method == "POST"):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })


class ProductViewset(APIView):
    #127.0.0.1:8000/products/id/
    def get(self, request):         #trying to access product that does not exist?
        if(request.GET.get('id')):
            product_id = request.GET.get('id')
            products = Products.objects.filter(pk = product_id)
            serialized=ProductSerializer(products, many=True).data
        else:
            products = Products.objects.all()
            serialized=ProductSerializer(products, many=True).data
        return JsonResponse({"products": serialized}, status=status.HTTP_200_OK)

    def post(self, request):
        post_data = request.data
        productObj = Products(p_name=post_data["p_name"], p_type=post_data["p_type"], p_cost=post_data["p_cost"], p_count=post_data["p_count"],
                      )
        productObj.save()
        print(productObj.id)
        for vender_ in post_data["vender"]:
            productObj.vender.add(vender_)  
        vendors = Vender.objects.all()
        for i in vendors:
            change_price = VendorCostSet()
            change_price.Changed_amount = post_data["p_cost"]
            change_price.product_key = productObj
            change_price.vendor_key = i
            change_price.save()
        productObj.save()

        return Response({"status":"Success"}, status.HTTP_200_OK)

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

    
class AddToCartViewset(APIView): #change to be done: create a cart automatically whean a customer is created
    #127.0.0.1:8000/carts/id/
    #get cart for all user or any user with given id

         # post not used for now 
    def post(self, request):
        post_data = request.data
        cartObj = Cart( c_quantity = post_data["c_quantity"], c_total = post_data["c_total"])
        CustomerObj = Customer.objects.get(pk = )
        #cartObj = Cart() -> create this, add products, take number as input(need new table here), and based on quantity calculate cost and total cost
        cartObj.save()
        print(cartObj.id)
        for product_ in post_data["c_product"]:
            cartObj.c_product.add(product_)  
            cartObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)
    
    def get(self, request):
        if(request.GET.get('id')):
            cart_id = request.GET.get('id')
            carts = Cart.objects.filter(pk = cart_id)
            #print(carts)
            serialized=CartSerializer(carts, many=True).data
        else:
            cart = Cart.objects.all()
            serialized=CartSerializer(cart, many=True).data
        return JsonResponse({"cart": serialized}, status=status.HTTP_200_OK)
    
    #delete product from a cart. 127.0.0.1:8000/products/id/ (given product id must be in cart to delete)
    def delete(self, request):
        if(request.GET.get('id')): # pass id in param
            cart_id = request.GET.get('id')     
            if(request.GET.get('c_product')):#pass c_product id number in param 
                delete = int(request.GET.get('c_product'))
                if delete not in list(Cart.objects.filter(pk=cart_id).values_list("c_product", flat = True)):
                    return Response({"status": "Failure"}, status=status.HTTP_400_BAD_REQUEST)

            del_product = request.GET.get("c_product")
            #print(del_product, request.GET.get('id'))
            carts1 = Cart.objects.filter(pk=cart_id)#.values_list("c_product", flat = True)
            for i in carts1:
                i.c_product.remove(del_product)
                i.save()
                #print(i, del_product) 
            # print(carts1.c_product)
            serialized=CartSerializer(carts1, many=True).data
        else:
            # cart = Cart.objects.all()
            # serialized=CartSerializer(cart, many=True).data
            Cart.objects.all().delete()
            return Response({"status": "deleted"}, status.HTTP_200_OK)
        return JsonResponse({"cart": serialized}, status=status.HTTP_200_OK)

    def put(self, request):
        product_id = request.GET.get('id') #product id to be added in params
        customer_id = request.GET.get("c_id") # customer id where it is to be added. cart and customer 1-1 relationship
        customer = Customer.objects.get(pk = customer_id)
        customer.cart.c_product.add(product_id)
        customer.save()
        customer = Customer.objects.filter(pk = customer_id)
        return Response({"status": "updated"}, status.HTTP_200_OK)


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
        if(request.GET.get('id')):
            vendor_id = request.GET.get('id')
            vendors = VendorCostSet.objects.filter(pk = vendor_id)
            print(vendors)
            serialized=VendorCostSerializer(vendors, many=True).data
        else:
            vendors = VendorCostSet.objects.all()
            print(vendors)
            serialized=VendorCostSerializer(vendors, many=True).data
        return JsonResponse({"vendors": serialized}, status=status.HTTP_200_OK)


    def put(self, request):
        new_amount = 120
        post_data = request.data
        vendor_id = request.GET.get('v_id')
        product_id = request.GET.get('p_id')
        entries = VendorCostSet.objects.get(vendor_key = vendor_id, product_key = product_id)
        entries.Changed_amount = new_amount
        entries.save()
        # for i in entries:
        #     print(i.Changed_amount)
        return Response({"status":"Success"}, status.HTTP_200_OK)


class OrderViewSet(APIView):
    def post(self, request):
        post_data = request.data
        order = Order(o_status = post_data["o_status"], c_cart = post_data["c_cart"])
        cartObj.save()
        print(cartObj.id)
        for product_ in post_data["c_vendor"]:
            order.o_vender.add(product_)  
            order.save()
        for product_ in post_data["c_user"]:
            order.o_user.add(product_)  
            order.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)
    
class BillViewSet(APIView):
    def get(self, request):
        customer_id = request.GET.get("c_id")
        customer = Customer.objects.get(pk = customer_id)
        cust_details = customer.cart.c_product.all()
        print(cust_details[1])
        #print(customer.cart.c_total)
        # bill = Bill()
        # bill.b_quantity = 10 #hardcoding for nwo
        # bill.b_amount = customer.cart.c_total
        # for product_ in customer.products:
        #     print(product_)
        return Response({"status":"Success"}, status.HTTP_200_OK    )        # return name, address, vendor name, vendor number, total amount,date
    

    #def delete(APIView):
        
 