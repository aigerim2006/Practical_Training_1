from django.contrib import admin
from .models import UserProgress

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'body_weight')
    list_filter = ('user', 'date')