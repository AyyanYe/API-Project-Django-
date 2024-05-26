# views.py
from rest_framework import generics, permissions, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from .models import MenuItem, Cart, Order, OrderItem
from .serializers import MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
from .filters import MenuItemFilter, OrderFilter
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework import serializers

class MenuItemList(generics.ListCreateAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_class = MenuItemFilter
    search_fields = ['title', 'category__title']
    ordering_fields = ['price', 'title']

    def get_queryset(self):
        return MenuItem.objects.all()

    def perform_create(self, serializer):
        if self.request.user.groups.filter(name='Manager').exists():
            serializer.save()
        else:
            raise PermissionDenied("Only managers can create menu items.")

class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.groups.filter(name='Manager').exists():
            return MenuItem.objects.all()
        else:
            raise NotFound("Item not found or you don't have permission.")

    def perform_update(self, serializer):
        if self.request.user.groups.filter(name='Manager').exists():
            serializer.save()
        else:
            raise PermissionDenied("Only managers can update menu items.")

    def perform_destroy(self, instance):
        if self.request.user.groups.filter(name='Manager').exists():
            instance.delete()
        else:
            raise PermissionDenied("Only managers can delete menu items.")

class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = OrderFilter
    ordering_fields = ['total', 'date']

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart_items = Cart.objects.filter(user=self.request.user)
        if not cart_items:
            raise serializers.ValidationError("No items in the cart.")
        
        order_total = sum(item.price for item in cart_items)
        serializer.save(user=self.request.user, total=order_total)
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=serializer.instance,
                menuitem=cart_item.menuitem,
                quantity=cart_item.quantity,
                unit_price=cart_item.unit_price,
                price=cart_item.price
            )
        Cart.objects.filter(user=self.request.user).delete()

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            return Order.objects.filter(delivery_crew=self.request.user)
        else:
            return Order.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        elif self.request.user.groups.filter(name='Delivery Crew').exists():
            if 'status' in serializer.validated_data:
                serializer.save()
            else:
                raise PermissionDenied("Delivery crew can only update the order status.")
        else:
            raise PermissionDenied("You don't have permission to update this order.")

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("Only staff can delete orders.")
