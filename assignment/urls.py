from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
                                            #access token       #refresh token
from product.views import HelloView
urlpatterns = [
    path('', include('product.urls')),
    path('admin/', admin.site.urls),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('hello/', HelloView.as_view(), name='hello')
]

#payload ?
#token based 
#s3
#dokers