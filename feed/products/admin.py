from django.contrib import admin
from feed.products.models import Category, Product
# Register your models here.

admin.site.register(Category)
admin.site.register(Product)

