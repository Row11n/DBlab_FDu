from django.urls import path, include
from . import views

app_name = 'Userinfo'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_for_staff/', views.register_for_staff, name='register_for_staff'),
    path('login/', views.loginView, name='login'),
    path('', include('django.contrib.auth.urls')),
    path('userinfo/<int:user_id>/', views.UserInfoView.as_view(), name='userinfo'),
]