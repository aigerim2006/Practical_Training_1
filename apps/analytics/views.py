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

        workouts = Workout.objects.filter(user=user, date__gte=month_ago).prefetch_related('exercises')
        progress_logs = UserProgress.objects.filter(user=user, date__gte=month_ago)

        total_stats = Workout.objects.filter(user=user).aggregate(
            sum_kcal=Sum('calories_burned'),
            count_id=Count('id')
        )

        # 1. Генерируем массив всех 30 дней для непрерывной оси X
        all_dates = [month_ago + datetime.timedelta(days=i) for i in range(31)]
        
        # 2. Группируем данные по датам для быстрого поиска
        workout_data = {}
        for w in workouts:
            if w.date not in workout_data:
                workout_data[w.date] = []
            workout_data[w.date].append(w)
            
        progress_data = {p.date: p for p in progress_logs}

        # 3. Формируем списки для графиков
        labels = []
        energy = []
        tonnages = []
        weights = []

        for d in all_dates:
            labels.append(d.strftime('%d.%m'))
            
            # Энергия и тоннаж (если в один день было несколько тренировок — суммируем)
            if d in workout_data:
                day_workouts = workout_data[d]
                day_kcal = sum(w.calories_burned or 0 for w in day_workouts)
                day_tonnage = sum(sum(e.get_tonnage() for e in w.exercises.all()) for w in day_workouts)
                energy.append(day_kcal)
                tonnages.append(day_tonnage)
            else:
                energy.append(0)
                tonnages.append(0)

            # Вес: если замера нет, кладем None (чтобы график не падал в ноль)
            if d in progress_data:
                weights.append(float(progress_data[d].body_weight))
            else:
                weights.append(None)

        context = {
            'total_calories': round(total_stats['sum_kcal'] or 0.0, 1),
            'total_workouts': total_stats['count_id'] or 0,
            'total_tonnage': round(sum(tonnages), 1),
            
            # Передаем данные в JSON. В dashboard.html используй эти переменные!
            'labels_list': json.dumps(labels),
            'energy_data': json.dumps(energy),
            'tonnage_data': json.dumps(tonnages),
            'weight_data': json.dumps(weights),
            
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