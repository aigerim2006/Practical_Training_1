import datetime
from django.db import transaction
from django.db.models import Sum, Count
from .models import Workout, ExerciseLog, UserProgress

class FitnessService:
    @staticmethod
    def calculate_burnt_calories(duration_minutes, workout_type_name):
        """
        Математический расчет расхода энергии (ТЗ 4.1.2 / Прецедент 2).
        Коэффициенты интенсивности физических нагрузок.
        """
        multiplier = 8.5 if workout_type_name == "Силовая" else 6.5
        return float(duration_minutes * multiplier)

    @staticmethod
    @transaction.atomic
    def register_workout_session(user, workout_date, workout_type, duration, exercises_data):
        """
        Сохранение комплексной сессии тренировок с гарантией целостности данных.
        """
        calories = FitnessService.calculate_burnt_calories(duration, workout_type.name)
        
        workout = Workout.objects.create(
            user=user,
            date=workout_date,
            type=workout_type,
            duration_minutes=duration,
            calories_burned=calories
        )

        for ex in exercises_data:
            if ex.get('exercise_name') and ex.get('sets'):
                ExerciseLog.objects.create(
                    workout=workout,
                    exercise_name=ex['exercise_name'],
                    sets=int(ex['sets']),
                    reps=int(ex['reps']),
                    weight=float(ex['weight'])
                )
        return workout

    @staticmethod
    def get_dashboard_analytics(user):
        """
        Агрегация статистических данных и подготовка выборок для Chart.js (ТЗ 4.1.3).
        """
        today = datetime.date.today()
        month_ago = today - datetime.timedelta(days=30)
        
        user_workouts = Workout.objects.filter(user=user, date__gte=month_ago).order_by('date')
        user_progress = UserProgress.objects.filter(user=user, date__gte=month_ago).order_by('date')

        # Суммарные агрегаты
        total_stats = Workout.objects.filter(user=user).aggregate(
            total_calories=Sum('calories_burned'),
            total_duration=Sum('duration_minutes'),
            workout_count=Count('id')
        )

        # Подготовка массивов для графиков JavaScript
        chart_workouts = {
            'dates': [w.date.strftime('%d.%m') for w in user_workouts],
            'calories': [w.calories_burned for w in user_workouts],
            'durations': [w.duration_minutes for w in user_workouts]
        }

        chart_weight = {
            'dates': [p.date.strftime('%d.%m') for p in user_progress],
            'weights': [p.body_weight for p in user_progress]
        }

        return {
            'total_calories': total_stats['total_calories'] or 0.0,
            'total_duration': total_stats['total_duration'] or 0,
            'workout_count': total_stats['workout_count'] or 0,
            'chart_workouts': chart_workouts,
            'chart_weight': chart_weight,
            'raw_workouts': Workout.objects.filter(user=user).order_by('-date')[:5]
        }