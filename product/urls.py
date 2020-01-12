from django.urls import path
from .views import ProductViewset, AddToCartViewset

urlpatterns = [
    path('products', ProductViewset.as_view()),
    path('carts', AddToCartViewset.as_view())
]