from django.contrib import admin
from .models import WorkoutType, Workout, ExerciseLog, UserProgress

class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 1

@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'type', 'duration_minutes', 'calories_burned')
    list_filter = ('type', 'date', 'user')
    search_fields = ('user__username', 'type__name')
    inlines = [ExerciseLogInline]

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'body_weight')
    list_filter = ('date', 'user')

admin.site.register(WorkoutType)