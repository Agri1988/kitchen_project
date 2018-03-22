from django.contrib import admin
from .models import MovingProducts, ProductsInDocument, DishInDocument

# Register your models here.
admin.site.register(MovingProducts)
admin.site.register(ProductsInDocument)
admin.site.register(DishInDocument)

