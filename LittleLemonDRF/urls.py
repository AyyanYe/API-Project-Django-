from django.urls import path, include
from .views import MenuItemList, CartView, MenuItemDetail, OrderView, OrderDetailView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
  

urlpatterns = [ 
    path('', include('djoser.urls')), 
    path('', include('djoser.urls.authtoken')), 
    path('token/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('menu-items/', MenuItemList.as_view(), name='menu-item-list'),
    path('menu-items/<int:pk>/', MenuItemDetail.as_view(), name='menu-item-detail'),
    path('cart/menu-items/', CartView.as_view(), name='cart'),
    path('orders/', OrderView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
] 