# filters.py
import django_filters
from .models import MenuItem, Order

class MenuItemFilter(django_filters.FilterSet):
    class Meta:
        model = MenuItem
        fields = ['category', 'featured', 'price']

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = ['status', 'delivery_crew', 'date']