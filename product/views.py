from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from product.models import Products, Vender, Order, Bill, Delivery, Customer, Cart
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer, CartSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse


import logging
logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py

class ProductViewset(APIView):
    #127.0.0.1:8000/products/id/
    def get(self, request):
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
            productObj.save()
        # for customer_ in post_data["customer"]:
        #     productObj.customer.add(customer_)
        #     productObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.GET.get('id')
        print(product_id)
        Products.objects.filter(pk=product_id).delete()
        return Response({"status": "deleted"}, status.HTTP_200_OK)

    def put(self, request):     #updates name
        product_id = request.GET.get('id')
        post_data = request.data
        productObj = Products.objects.filter(pk=product_id)
        # print(productObj.id)
        # print(productObj.p_name) #= post_data["p_name"]
        #productObj.p_name = "adslaklads"
        #serializer = ProductSerializer(productObj, data = request.data)
        for i in productObj:    #any other way?
            # i.p_name = "Athreya"
            i.p_name = post_data["p_name"]
            i.save(update_fields=["p_name"])
        #productObj(productObj.id)
        return Response({"status": "updated"}, status.HTTP_200_OK)

    




class AddToCartViewset(APIView):
    #127.0.0.1:8000/carts/id/

    # post not used for now 
    def post(self, request):
        post_data = request.data
        #customer_id = Customer.objects.get(c_name = post_data["user_name"]).id
        cartObj = Cart( c_quantity = post_data["c_quantity"], c_total = post_data["c_total"])
        cartObj.save()
        print(cartObj.id)
        for product_ in post_data["c_product"]:
            cartObj.c_product.add(product_)  
            cartObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)

    #get cart for all user or any user with given id
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
            #carts = Cart.objects.filter(pk = cart_id)
            carts1 = Cart.objects.filter(pk=cart_id)#.values_list("c_product", flat = True)
            #print(carts)
            for i in carts1:
                i.c_product.remove(del_product)
                i.save()
                #print(i, del_product) 
            # print(carts)
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


    '''
    Post body json:
     {
            "p_name": "Parker",
            "p_type": "Pen",
            "p_cost": "250.00",
            "p_count": 213,
            "vender": [
                2
            ],
            "customer": []
     }
     Study: https://docs.djangoproject.com/en/3.0/topics/db/examples/many_to_many/
    '''