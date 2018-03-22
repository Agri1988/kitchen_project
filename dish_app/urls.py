from django.urls import path, include
from . import views
from  . import forms

app_name = 'dish_app'
urlpatterns = [
    path('all_dishes/', views.all_dishes, name='all_dishes'),
    path('detail_dish/<int:dish_id>/', views.detail_dish, name='detail_dish'),
    path('new_dish/', views.detail_dish, name='new_dish'),
    path('all_products/', views.all_products, name='all_products'),
    path('detail_product/<int:product_id>', views.detail_product, name='detail_product'),
    path('new_product/', views.detail_product, name='new_product'),
    path('product_to_productList/', views.detail_product, name='product_to_productList'),
    path('add_product_to_dish/', views.add_product_to_dish, name='add_product_to_dish'),
    path('add_product_category', views.add_field_element,{'form':forms.ProductCategoryForm,
                                                  'template':'dish_app/add_category_product.html',
                                                  'fieldname': 'name'},
                                                    name='add_product_category'),
    path('add_dish_category', views.add_field_element,{'form':forms.DishCategoryForm,
                                                  'template':'dish_app/add_category_dish.html',
                                                  'fieldname': 'name'},
                                                    name='add_dish_category'),
]
