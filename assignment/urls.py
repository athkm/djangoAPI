
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
                                            #access token       #refresh token

urlpatterns = [
    path('', include('product.urls')),
    path('admin/', admin.site.urls),
   path('token/', TokenObtainPairView.as_view()),
    path('token/', TokenRefreshView.as_view())
]
