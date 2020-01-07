from django.shortcuts import render

# Create your views here.
from product.models import Products, Vender, Order, Bill, Delivery, Customer
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer, VenderSerializer, CustomerSerializer, BillSerializer, OrderSerializer, DeliverySerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = Products.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProductSerializer


class VenderViewset(viewsets.ModelViewSet):
    queryset = Vender.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = VenderSerializer

class CustomerViewset(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = CustomerSerializer

class BillViewset(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = BillSerializer

class OrderViewset(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = OrderSerializer

class DeliveryViewset(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DeliverySerializer