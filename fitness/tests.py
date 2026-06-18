from django.test import TestCase
from django.contrib.auth.models import User
from fitness.models import WorkoutType, Workout, UserProgress
from fitness.services import FitnessService

class FitnessCoreTestCase(TestCase):
    def setUp(self):
        self.user_alex = User.objects.create_user(username="alex", email="alex@test.com", password="password123")
        self.user_mira = User.objects.create_user(username="mira", email="mira@test.com", password="password123")
        
        self.cardio_type = WorkoutType.objects.create(name="Бег", description="Кардио сессии")
        self.strength_type = WorkoutType.objects.create(name="Силовая", description="Работа со снарядами")

        UserProgress.objects.create(user=self.user_alex, date="2026-06-10", body_weight=80.0, notes="Старт")
        UserProgress.objects.create(user=self.user_mira, date="2026-06-10", body_weight=60.0, notes="Старт")

    def test_calorie_calculator_precision_by_met(self):
        """Проверка точности формулы MET, учитывающей индивидуальный вес атлета"""
        calories_alex_cardio = FitnessService.calculate_burnt_calories(60, "Бег", 80.0)
        # 9.8 * 3.5 * 80 / 200 * 60 = 823.2
        self.assertEqual(calories_alex_cardio, 823.2)

    def test_data_isolation_security(self):
        """Проверка нефункционального требования безопасности: изоляция данных пользователей"""
        FitnessService.register_workout_session(
            user=self.user_alex, workout_date="2026-06-15",
            workout_type=self.cardio_type, duration=45, exercises_data=[]
        )
        
        analytics_alex = FitnessService.get_dashboard_analytics(self.user_alex)
        analytics_mira = FitnessService.get_dashboard_analytics(self.user_mira)
        
        self.assertEqual(analytics_alex['workout_count'], 1)
        self.assertEqual(analytics_mira['workout_count'], 0)