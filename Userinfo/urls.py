from django.urls import path, include
from . import views

app_name = 'Userinfo'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
    path('', include('django.contrib.auth.urls')),
]