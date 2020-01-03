from product.models import Product
from rest_framework import viewsets, permissions
from .serializers import ProductSerializer

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ProductSerializer