from django.db import models
from django.contrib.auth.models import User

class WorkoutType(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название активности")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Тип тренировки"
        verbose_name_plural = "Типы тренировок"

    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts', verbose_name="Пользователь")
    date = models.DateField(verbose_name="Дата проведения")
    type = models.ForeignKey(WorkoutType, on_delete=models.PROTECT, verbose_name="Тип активности")
    duration_minutes = models.PositiveIntegerField(verbose_name="Длительность (мин)")
    calories_burned = models.FloatField(verbose_name="Сожженные калории")

    class Meta:
        verbose_name = "Тренировка"
        verbose_name_plural = "Тренировки"
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.type.name} ({self.date})"

class ExerciseLog(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises', verbose_name="Тренировка")
    exercise_name = models.CharField(max_length=100, verbose_name="Название упражнения")
    sets = models.PositiveIntegerField(verbose_name="Подходы")
    reps = models.PositiveIntegerField(verbose_name="Повторения")
    weight = models.FloatField(verbose_name="Рабочий вес (кг)")

    class Meta:
        verbose_name = "Журнал упражнения"
        verbose_name_plural = "Журналы упражнений"

    def __str__(self):
        return f"{self.exercise_name}: {self.sets}x{self.reps} @ {self.weight} кг"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_logs', verbose_name="Пользователь")
    date = models.DateField(verbose_name="Дата замера")
    body_weight = models.FloatField(verbose_name="Масса тела (кг)")
    notes = models.TextField(blank=True, null=True, verbose_name="Заметки")

    class Meta:
        verbose_name = "Прогресс пользователя"
        verbose_name_plural = "Прогресс пользователей"
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.body_weight} кг ({self.date})"