from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('workout/add/', views.add_workout_view, name='add_workout'),
    path('workout/<int:pk>/delete/', views.delete_workout_view, name='delete_workout'),
]