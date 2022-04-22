from django.urls import path
from . import views

app_name = 'system'

urlpatterns = [
    path('', views.home, name='home'),
]