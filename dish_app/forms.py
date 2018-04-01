from django import forms
from .models import Dish, Product, ProductCategory, Category, Ingredients


class DishForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"


class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class DishCategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredients
        fields = "__all__"