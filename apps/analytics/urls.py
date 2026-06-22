from django.urls import path
from .views import DashboardView, ProgressLogView, AchievementsView, EditProgressView, DeleteProgressView

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('progress/', ProgressLogView.as_view(), name='progress_log'),
    path('progress/<int:pk>/edit/', EditProgressView.as_view(), name='edit_progress'),
    path('progress/<int:pk>/delete/', DeleteProgressView.as_view(), name='delete_progress'),
    path('achievements/', AchievementsView.as_view(), name='achievements'),
]
