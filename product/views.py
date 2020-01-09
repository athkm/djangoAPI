from django.shortcuts import render
from rest_framework.views import APIView
# Create your views here.
from product.models import Products, Vender, Order, Bill, Delivery, Customer
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

import logging
logger = logging.getLogger('app_api') #from LOGGING.loggers in settings.py

class ProductViewset(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Products.objects.all()
    # def list(self, request):
    #     queryset = Products.objects.all()
    #     logging.info('Hello')
    #     serializer = ProductSerializer(queryset, many=True)
    #     return Response(serializer.data)

    # def retrieve(self, request, pk=None):
    #     logging.info('Hello')
    #     queryset = Products.objects.all()
    #     user = get_object_or_404(queryset, pk=pk)
    #     serializer = ProductSerializer(user)
    #     return Response(serializer.data)


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