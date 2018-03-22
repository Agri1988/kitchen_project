from django import forms
from .models import Document, ProductsInDocument, DishInDocument

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class ProductInDocumentsForm(forms.ModelForm):
    class Meta:
        model = ProductsInDocument
        exclude = ['document']



class DishInDocumentForm(forms.ModelForm):
    class Meta:
        model = DishInDocument
        exclude = ['document']