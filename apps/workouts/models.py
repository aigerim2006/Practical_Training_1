from django.db import models
from django.contrib.auth.models import User

class WorkoutType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    met_coefficient = models.FloatField(default=5.0, help_text="Используется для точного расчета ккал по формуле MET")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тип тренировки'
        verbose_name_plural = 'Типы тренировок'

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    type = models.ForeignKey(WorkoutType, on_delete=models.PROTECT)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.FloatField()

    class Meta:
        verbose_name = 'Тренировка'
        verbose_name_plural = 'Тренировки'
        ordering = ['-date']

class ExerciseLog(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def get_tonnage(self):
        return self.sets * self.reps * self.weight
    
    class Meta:
        verbose_name = 'Упражнение'
        verbose_name_plural = 'Упражнения'