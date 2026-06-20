from django.urls import path
from .views import WorkoutListView, WorkoutDetailView, AddWorkoutView, DeleteWorkoutView

app_name = 'workouts' # Это позволит использовать префикс 'workouts:'

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
    path('add/', AddWorkoutView.as_view(), name='workout_add'),
    path('<int:pk>/delete/', DeleteWorkoutView.as_view(), name='workout_delete'),
]