from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()
    min_price = filters.NumberFilter(name="price", lookup_type='gte')
    max_price = filters.NumberFilter(name="price", lookup_type='lte')
    title = filters.CharFilter()
    class Meta:
        model = Product
        fields = ('price', 'min_price', 'max_price', 'title')