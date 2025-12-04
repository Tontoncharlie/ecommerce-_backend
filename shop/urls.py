from django.urls import path, include
from rest_framework import routers
from .views import ProductViewSet, RegisterAPIView, LoginAPIView, CartAPIView, OrderAPIView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('order/', OrderAPIView.as_view(), name='order')
]