from django.urls import path, include
from . import views

app_name = 'base_app'
urlpatterns = [
    path('', views.index, name='index')

]
