from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from product.models import Products, Vender, Order, Bill, Delivery, Customer
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
import json
from django.http import JsonResponse


import logging
logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py

class ProductViewset(APIView):
    # serializer_class = ProductSerializer
    # queryset = Products.objects.all()
    # def list(self, request):
    #     queryset = Products.objects.all()
    #     logging.info('Hello')
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     logging.info('Hello')
    #     queryset = Products.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = ProductSerializer(user)
    #     return Response(serializer.data)

    #Get all product data. url: 127.0.0.1:8000/api/products/
    def get(self, request):
        products = Products.objects.all()
        serialized=ProductSerializer(products, many=True).data
        return JsonResponse({"products": serialized}, status=status.HTTP_200_OK)

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
    def post(self, request):
        post_data = request.data
        productObj = Products(p_name=post_data["p_name"], p_type=post_data["p_type"], p_cost=post_data["p_cost"], p_count=post_data["p_count"],
                      )
        productObj.save()
        print(productObj.id)
        for vender_ in post_data["vender"]:
            productObj.vender.add(vender_)
            productObj.save()
        for customer_ in post_data["customer"]:
            productObj.customer.add(customer_)
            productObj.save()
        return Response({"status":"Success"}, status.HTTP_200_OK)

    def delete(self, request):
        product_id = request.GET.get('id')
        print(product_id)
        Products.objects.filter(pk=product_id).delete()
        return Response({"status": "deleted"}, status.HTTP_200_OK)

    def put(self, request):
        product_id = request.GET.get('id')
        post_data = request.data
        productObj = Products.objects.get(pk=product_id)
        print(productObj.id)
        productObj["p_name"] = post_data["p_name"]
        productObj.save(update_fields=["p_name"])
        productObj(productObj.id)
        return Response({"status": "updated"}, status.HTTP_200_OK)




# class VenderViewset(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Products, pk=pk)
#         data = PollSerializer(Products).data
#         return Response(data)

# class ProductViewset(viewsets.ModelViewSet):
#     queryset = Products.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = ProductSerializer

# class VenderViewset(viewsets.ModelViewSet):
#     queryset = Vender.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = VenderSerializer

# class CustomerViewset(viewsets.ModelViewSet):
#     queryset = Customer.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = CustomerSerializer

# class BillViewset(viewsets.ModelViewSet):
#     queryset = Bill.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = BillSerializer

# class OrderViewset(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = OrderSerializer

# class DeliveryViewset(viewsets.ModelViewSet):
#     queryset = Delivery.objects.all()
#     permission_classes = [
#         permissions.AllowAny
#     ]
#     serializer_class = DeliverySerializer