import datetime
from django.db import transaction
from django.db.models import Sum, Count
from .models import Workout, ExerciseLog, UserProgress, WorkoutType

class FitnessService:
    MET_COEFFICIENTS = {
        "Бег": 9.8,
        "Силовая": 6.0,
        "Йога": 3.0,
        "Кроссфит": 8.0
    }

    @staticmethod
    def calculate_burnt_calories(duration_minutes, workout_type_name, user_weight):
        """
        Расчет по формуле: Энергозатраты = MET * 3.5 * Вес (кг) / 200 * Минуты
        Исключает генерацию нулевых и абстрактных значений.
        """
        met = FitnessService.MET_COEFFICIENTS.get(workout_type_name, 5.0)
        return round(float(met * 3.5 * user_weight / 200.0 * duration_minutes), 1)

    @staticmethod
    @transaction.atomic
    def register_workout_session(user, workout_date, workout_type, duration, exercises_data):
        """
        Атомарная регистрация тренировки. Если падает запись упражнения — сессия откатывается полностью.
        """
        # Извлекаем последний актуальный вес пользователя для точного расчета MET
        latest_progress = UserProgress.objects.filter(user=user, date__lte=workout_date).order_by('-date').first()
        weight = latest_progress.body_weight if latest_progress else 70.0 # Дефолтный физиологический вес

        calories = FitnessService.calculate_burnt_calories(duration, workout_type.name, weight)
        
        workout = Workout.objects.create(
            user=user, date=workout_date, type=workout_type,
            duration_minutes=duration, calories_burned=calories
        )

        for ex in exercises_data:
            if ex.get('exercise_name').strip():
                ExerciseLog.objects.create(
                    workout=workout,
                    exercise_name=ex['exercise_name'].strip(),
                    sets=int(ex['sets']),
                    reps=int(ex['reps']),
                    weight=float(ex['weight'])
                )
        return workout

    @staticmethod
    def get_dashboard_analytics(user):
        """
        Агрегация данных за последние 30 дней для построения графиков Chart.js (ТЗ п. 4.1.3).
        """
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=30)
        
        # Получаем выборки с оптимизацией запросов prefetch_related
        user_workouts = Workout.objects.filter(user=user, date__gte=month_ago).prefetch_related('exercises').order_by('date')
        user_progress = UserProgress.objects.filter(user=user, date__gte=month_ago).order_by('date')

        total_stats = Workout.objects.filter(user=user).aggregate(
            total_calories=Sum('calories_burned'),
            total_duration=Sum('duration_minutes'),
            workout_count=Count('id')
        )

        # Вычисление динамики изменения веса снарядов (Тоннаж = Подходы * Повторения * Вес)
        dates, calories, tonnages = [], [], []
        for w in user_workouts:
            dates.append(w.date.strftime('%d.%m'))
            calories.append(w.calories_burned)
            
            workout_tonnage = sum(ex.sets * ex.reps * ex.weight for ex in w.exercises.all())
            tonnages.append(round(workout_tonnage, 1))

        return {
            'total_calories': round(total_stats['total_calories'] or 0.0, 1),
            'total_duration': total_stats['total_duration'] or 0,
            'workout_count': total_stats['workout_count'] or 0,
            'chart_workouts': {'dates': dates, 'calories': calories},
            'chart_weight': {
                'dates': [p.date.strftime('%d.%m') for p in user_progress],
                'weights': [p.body_weight for p in user_progress]
            },
            'chart_tonnage': {'dates': dates, 'tonnages': tonnages},
            'raw_workouts': Workout.objects.filter(user=user).order_by('-date')[:10]
        }