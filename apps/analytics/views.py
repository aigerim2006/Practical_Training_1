import json
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from apps.workouts.models import Workout
from .models import UserProgress
from .forms import UserProgressForm
import datetime
from django.shortcuts import render


class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=30)

        # Оптимизированные SQL запросы агрегации данных
        workouts = Workout.objects.filter(user=user, date__gte=month_ago).prefetch_related('exercises').order_by('date')
        progress_logs = UserProgress.objects.filter(user=user, date__gte=month_ago).order_by('date')

        total_stats = Workout.objects.filter(user=user).aggregate(
            sum_kcal=Sum('calories_burned'),
            count_id=Count('id')
        )

        # Подготовка сериализованных данных под Chart.js (Исключает ошибки дублирования JS)
        workout_dates = [w.date.strftime('%d.%m') for w in workouts]
        workout_calories = [w.calories_burned for w in workouts]
        tonnages = [sum(e.get_tonnage() for e in w.exercises.all()) for w in workouts]

        weight_dates = [p.date.strftime('%d.%m') for p in progress_logs]
        weight_values = [p.body_weight for p in progress_logs]

        context = {
            'total_calories': round(total_stats['sum_kcal'] or 0.0, 1),
            'total_workouts': total_stats['count_id'] or 0,
            
            # Маршализация в JSON строки для безопасной вставки в шаблоны
            'w_dates_json': json.dumps(workout_dates),
            'w_kcal_json': json.dumps(workout_calories),
            'w_tonnage_json': json.dumps(tonnages),
            'p_dates_json': json.dumps(weight_dates),
            'p_weights_json': json.dumps(weight_values),
            'recent_workouts': Workout.objects.filter(user=user).order_by('-date')[:5]
        }
        return render(request, 'analytics/dashboard.html', context)

class ProgressLogView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserProgressForm()
        logs = UserProgress.objects.filter(user=request.user).order_by('-date')
        return render(request, 'analytics/progress_log.html', {'form': form, 'logs': logs})

    def post(self, request):
        form = UserProgressForm(request.POST)
        if form.is_valid():
            progress = form.save(commit=False)
            progress.user = request.user
            progress.save()
            return redirect('analytics:progress_log')
        return render(request, 'analytics/progress_log.html', {'form': form})
    
class AchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/achievements.html'

def home(request):
    return render(request, 'home.html')
