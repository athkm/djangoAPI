from rest_framework import routers
from .views import ProductViewset, VenderViewset
from django.urls import path
router = routers.DefaultRouter()
router.register('product', ProductViewset, 'product')
router.register('vender', VenderViewset, 'vender')
urlpatterns = router.urls


# urlpatterns = [
#     # path('', include('product.urls')),
#     # path('admin/', admin.site.urls),
#     path('product/', ProductViewset, name = 'product'),
#     path('vender/', VenderViewset, name = 'vender')
# ]