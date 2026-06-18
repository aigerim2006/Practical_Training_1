from django.test import TestCase
from django.contrib.auth.models import User
from fitness.models import WorkoutType, Workout
from fitness.services import FitnessService

class FitnessCoreTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="alex", email="alex@test.com", password="password123")
        self.user2 = User.objects.create_user(username="mira", email="mira@test.com", password="password123")
        self.cardio_type = WorkoutType.objects.create(name="Кардио", description="Бег/Велосипед")
        self.strength_type = WorkoutType.objects.create(name="Силовая", description="Тяжелая атлетика")

    def test_calorie_calculator_precision(self):
        """Проверка точности изолированных математических расчетов калорий"""
        calories_cardio = FitnessService.calculate_burnt_calories(40, self.cardio_type)
        calories_strength = FitnessService.calculate_burnt_calories(40, self.strength_type)
        
        self.assertEqual(calories_cardio, float(40 * 6.5))
        self.assertEqual(calories_strength, float(40 * 8.5))

    def test_data_isolation_security(self):
        """Проверка изоляции данных (ТЗ 4.3): Пользователи видят только свои логи"""
        FitnessService.register_workout_session(
            user=self.user1,
            workout_date="2026-06-15",
            workout_type=self.cardio_type,
            duration=30,
            exercises_data=[]
        )
        
        analytics_user1 = FitnessService.get_dashboard_analytics(self.user1)
        analytics_user2 = FitnessService.get_dashboard_analytics(self.user2)
        
        self.assertEqual(analytics_user1['workout_count'], 1)
        self.assertEqual(analytics_user2['workout_count'], 0)