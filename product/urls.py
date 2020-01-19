from django.urls import path, include
from .views import ProductViewset, AddToCartViewset, VendorViewset, home, signup, BillViewSet

urlpatterns = [
    path('products', ProductViewset.as_view()),
    path('carts', AddToCartViewset.as_view()),
    path('vendors', VendorViewset.as_view()),
    path('', home, name = "home"),
    path('bill', BillViewSet.as_view()),
    path('account/', include('django.contrib.auth.urls')),#, name = "login"),
    path('signup/', signup, name = "signup"),
    # path('account/', include('django.contrib.auth.urls')),
]