from django.contrib import admin
from .models import WorkoutType, Workout, ExerciseLog, UserProgress

class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'type', 'duration_minutes', 'calories_burned')
    list_filter = ('type', 'date')
    inlines = [ExerciseLogInline]

admin.site.register(WorkoutType)
admin.site.register(UserProgress)
