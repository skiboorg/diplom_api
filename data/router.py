from rest_framework import routers
from .views import *

router = routers.SimpleRouter(trailing_slash=False)
router.register(r'order', OrderViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'direction', DirectionViewSet)
router.register(r'country', CountryViewSet)
router.register(r'service', ServiceViewSet)
