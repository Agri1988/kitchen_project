from django.urls import path, include
from django.contrib.auth.views import login
from . import views

app_name = 'users_app'
urlpatterns = [
    path('login/', login, {'template_name':'users_app/login.html'}, name='login'),
    path('logout/', views.logout_view, name='logout'),

]
