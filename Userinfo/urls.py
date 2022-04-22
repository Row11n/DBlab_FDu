from django.urls import path
from . import views

app_name = 'Userinfo'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.loginView, name='login'),
]