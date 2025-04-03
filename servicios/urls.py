from django.urls import path, include 
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'carros', carroViewSet)
router.register(r'marcas', marcaViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('api/', include(router.urls)),

    path('api/carros/marca/<str:marca_nombre>/', CarrosPorMarcaView.as_view(), name='carros-por-marca'),
    path('api/carros/insertar/', InsertarCarroView.as_view(), name='insertar-carro'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]