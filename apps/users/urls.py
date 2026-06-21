from django.urls import path
from django.contrib.auth.views import LoginView # Импортируем стандартный логин
from . import views

app_name = 'users'

urlpatterns = [
    # Используем встроенный логин Django с твоим шаблоном
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    
    # Твои классы из views.py
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

