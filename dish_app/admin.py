from django.contrib import admin
from .models import Dish, Product, Ingredients, Category, ProductCategory

# Register your models here.
admin.site.register(Dish)
admin.site.register(Product)
admin.site.register(Ingredients)
admin.site.register(Category)
admin.site.register(ProductCategory)