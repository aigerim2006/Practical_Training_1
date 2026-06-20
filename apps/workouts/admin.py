from django.contrib import admin
from .models import Workout, WorkoutType, ExerciseLog

@admin.register(WorkoutType)
class WorkoutTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'met_coefficient')

class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'type', 'duration_minutes', 'calories_burned')
    list_filter = ('date', 'type')
    inlines = [ExerciseLogInline]

admin.site.register(ExerciseLog)