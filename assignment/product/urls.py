from rest_framework import routers
from .api import ProductViewset

router = routers.DefaultRouter()
router.register('api/product', ProductViewset, 'product')

urlpatterns = router.urls