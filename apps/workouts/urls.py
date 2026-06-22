from django.urls import path
from .views import (WorkoutListView, WorkoutDetailView, AddWorkoutView, UpdateWorkoutView,
                    DeleteWorkoutView, ScheduleView, add_schedule_view, 
                    DeleteScheduleView, UpdateScheduleView) # Импортируем UpdateView

app_name = 'workouts'

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('<int:pk>/', WorkoutDetailView.as_view(), name='workout_detail'),
    path('add/', AddWorkoutView.as_view(), name='workout_add'),
    path('<int:pk>/edit/', UpdateWorkoutView.as_view(), name='workout_edit'),
    path('<int:pk>/delete/', DeleteWorkoutView.as_view(), name='workout_delete'),
    path('schedule/', ScheduleView.as_view(), name='schedule'),
    path('schedule/add/', add_schedule_view, name='add_schedule'),
    path('schedule/<int:pk>/delete/', DeleteScheduleView.as_view(), name='delete_schedule'),
    path('schedule/<int:pk>/edit/', UpdateScheduleView.as_view(), name='edit_schedule'), 
]