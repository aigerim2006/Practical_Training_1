import json
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from apps.workouts.models import Workout
from .models import UserProgress
from .forms import UserProgressForm
from django.db.models import Min, Max, Avg

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
    
class AchievementsView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        
        # Сбор базовой статистики для расчета достижений
        total_workouts = Workout.objects.filter(user=user).count()
        total_calories = Workout.objects.filter(user=user).aggregate(sum_kcal=Sum('calories_burned'))['sum_kcal'] or 0
        total_logs = UserProgress.objects.filter(user=user).count()
        
        # Рассчитываем суммарный тоннаж всех упражнений
        workouts = Workout.objects.filter(user=user).prefetch_related('exercises')
        total_tonnage = sum(sum(e.get_tonnage() for e in w.exercises.all()) for w in workouts)

        # Система Геймификации: Очки опыта (XP) и Уровни
        # 1 тренировка = 100 XP, 1 замер веса = 25 XP, 100 ккал = 10 XP
        xp_from_workouts = total_workouts * 100
        xp_from_logs = total_logs * 25
        xp_from_calories = int(total_calories / 10)
        total_xp = xp_from_workouts + xp_from_logs + xp_from_calories
        
        # Расчет уровня (каждые 500 XP — новый уровень)
        user_level = (total_xp // 500) + 1
        xp_in_current_level = total_xp % 500
        xp_for_next_level = 500
        level_progress_percent = int((xp_in_current_level / xp_for_next_level) * 100)

        # Определение ранга атлета
        if user_level < 3:
            rank_name = "Новичок"
            rank_color = "from-slate-400 to-slate-500"
        elif user_level < 7:
            rank_name = "Продвинутый"
            rank_color = "from-indigo-400 to-cyan-400"
        elif user_level < 12:
            rank_name = "Элита"
            rank_color = "from-amber-400 to-orange-500"
        else:
            rank_name = "Легенда 🔥"
            rank_color = "from-purple-500 via-pink-500 to-rose-500"

        # Структурируем массив достижений (Ачивок)
        achievements_list = [
            {
                "id": "first_step",
                "title": "Первый шаг",
                "description": "Провести самую первую тренировку в системе",
                "icon": "🔥",
                "target": 1,
                "current": total_workouts,
                "progress_percent": min(int((total_workouts / 1) * 100), 100),
                "is_unlocked": total_workouts >= 1,
                "reward_xp": 100,
                "category": "Активность"
            },
            {
                "id": "iron_will",
                "title": "Стальная воля",
                "description": "Успешно выполнить 10 тренировок",
                "icon": "⚡",
                "target": 10,
                "current": total_workouts,
                "progress_percent": min(int((total_workouts / 10) * 100), 100),
                "is_unlocked": total_workouts >= 10,
                "reward_xp": 300,
                "category": "Активность"
            },
            {
                "id": "calorie_burner",
                "title": "Сжигатель жира",
                "description": "Сжечь в сумме 5,000 килокалорий",
                "icon": "☄️",
                "target": 5000,
                "current": int(total_calories),
                "progress_percent": min(int((total_calories / 5000) * 100), 100),
                "is_unlocked": total_calories >= 5000,
                "reward_xp": 400,
                "category": "Выносливость"
            },
            {
                "id": "titanium_lift",
                "title": "Титановый подъем",
                "description": "Поднять суммарный тоннаж в 15,000 кг",
                "icon": "🏋️",
                "target": 15000,
                "current": int(total_tonnage),
                "progress_percent": min(int((total_tonnage / 15000) * 100), 100),
                "is_unlocked": total_tonnage >= 15000,
                "reward_xp": 500,
                "category": "Сила"
            },
        ]

        # Подсчет количества открытых ачивок
        unlocked_count = sum(1 for a in achievements_list if a["is_unlocked"])

        context = {
            'achievements': achievements_list,
            'total_xp': total_xp,
            'user_level': user_level,
            'xp_in_current_level': xp_in_current_level,
            'xp_for_next_level': xp_for_next_level,
            'level_progress_percent': level_progress_percent,
            'rank_name': rank_name,
            'rank_color': rank_color,
            'unlocked_count': unlocked_count,
            'total_count': len(achievements_list),
        }
        return render(request, 'analytics/achievements.html', context)
    
class EditProgressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        progress = get_object_or_404(UserProgress, pk=pk, user=request.user)
        form = UserProgressForm(instance=progress)
        return render(request, 'analytics/progress_edit.html', {'form': form, 'progress': progress})

    def post(self, request, pk):
        progress = get_object_or_404(UserProgress, pk=pk, user=request.user)
        form = UserProgressForm(request.POST, instance=progress)
        if form.is_valid():
            form.save()
            return redirect('analytics:progress_log')
        return render(request, 'analytics/progress_edit.html', {'form': form, 'progress': progress})


class DeleteProgressView(LoginRequiredMixin, View):
    def post(self, request, pk):
        progress = get_object_or_404(UserProgress, pk=pk, user=request.user)
        progress.delete()
        return redirect('analytics:progress_log')

def progress_log(request):
    logs = UserProgress.objects.filter(user=request.user).order_by('-date')
    
    # Считаем агрегации
    stats = {}
    if logs.exists():
        stats['current'] = logs.first().body_weight
        stats['min'] = logs.aggregate(Min('body_weight'))['body_weight__min']
        stats['max'] = logs.aggregate(Max('body_weight'))['body_weight__max']
        
        first_weight = logs.last().body_weight
        stats['diff'] = round(stats['current'] - first_weight, 1)
    
    # Для графика (сортируем от старых к новым)
    chart_logs = logs.order_by('date')
    chart_labels = [log.date.strftime('%d.%m') for log in chart_logs]
    chart_data = [float(log.body_weight) for log in chart_logs]

    return render(request, 'analytics/progress_log.html', {
        'form': UserProgressForm(),
        'logs': logs,
        'stats': stats,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    })

def home(request):
    return render(request, 'home.html')