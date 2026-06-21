import json
import datetime
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from apps.workouts.models import Workout
from .models import UserProgress
from .forms import UserProgressForm

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=30)

        # Вытаскиваем тренировки за последние 30 дней
        workouts = Workout.objects.filter(user=user, date__gte=month_ago).prefetch_related('exercises').order_by('date')
        progress_logs = UserProgress.objects.filter(user=user, date__gte=month_ago).order_by('date')

        # Статистика за всё время (или можно поменять на month_ago, если нужна стата за месяц)
        total_stats = Workout.objects.filter(user=user).aggregate(
            sum_kcal=Sum('calories_burned'),
            count_id=Count('id')
        )

        # Списки для графиков
        workout_dates = [w.date.strftime('%d.%m') for w in workouts]
        workout_calories = [w.calories_burned for w in workouts]
        tonnages = [sum(e.get_tonnage() for e in w.exercises.all()) for w in workouts]

        weight_dates = [p.date.strftime('%d.%m') for p in progress_logs]
        weight_values = [p.body_weight for p in progress_logs]

        # Подсчет общего тоннажа за 30 дней
        total_tonnage = sum(tonnages) if tonnages else 0

        context = {
            'total_calories': round(total_stats['sum_kcal'] or 0.0, 1),
            'total_workouts': total_stats['count_id'] or 0,
            'total_tonnage': round(total_tonnage, 1),
            
            # Данные для Chart.js
            'w_dates_json': json.dumps(workout_dates),
            'w_kcal_json': json.dumps(workout_calories),
            'w_tonnage_json': json.dumps(tonnages),
            'p_dates_json': json.dumps(weight_dates),
            'p_weights_json': json.dumps(weight_values),
            
            # Передаем последние тренировки для истории
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
        logs = UserProgress.objects.filter(user=request.user).order_by('-date')
        return render(request, 'analytics/progress_log.html', {'form': form, 'logs': logs})
    
class AchievementsView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/achievements.html'

def home(request):
    return render(request, 'home.html')