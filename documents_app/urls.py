from django.urls import path, include
from . import views

app_name = 'documents_app'
urlpatterns = [
    path('all_documents/', views.all_documents, name='all_documents'),
    path('new_document/', views.detail_document, name='new_document'),
    path('detail_document/<int:document_id>', views.detail_document, name='detail_document'),
    path('get_all_dishes_to_document/', views.get_all_dishes_to_document, name='get_all_dishes_to_document'),
    path('get_all_products_to_document/', views.get_all_products_to_document, name='get_all_products_to_document'),
    path('products_remnants/', views.products_remnants, name='products_remnants'),
    path('products_remnants/<str:document_date>/', views.products_remnants, name='products_remnants'),
    path('report_day_income/', views.get_day_income, name='report_day_income'),
]
