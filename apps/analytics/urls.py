from django.urls import path
from .views import DashboardView, ProgressLogView,AchievementsView

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('progress/', ProgressLogView.as_view(), name='progress_log'),
    path('achievements/', AchievementsView.as_view(), name='achievements'),
]