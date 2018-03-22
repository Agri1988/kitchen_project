from django.shortcuts import render
from django.contrib.auth.views import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse
#from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users_app:login'))
