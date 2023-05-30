
from rest_framework import generics

from feed.products.filters import ProductFilter
from feed.products.serializers import ProductValidateSerializer
from rest_framework.pagination import PageNumberPagination
from feed.products.models import Product
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend




class ProductAPI(generics.ListCreateAPIView):
    serializer_class = ProductValidateSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('category_id', 'title', 'price')
    search_fields = ('title', 'price')
    filter_class = ProductFilter

class ProductDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductValidateSerializer
    queryset = Product.objects.all()
    pagination_class = PageNumberPagination

