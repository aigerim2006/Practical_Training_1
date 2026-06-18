from django.db import models
from django.contrib.auth.models import User

class WorkoutType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
    date = models.DateField()
    type = models.ForeignKey(WorkoutType, on_delete=models.PROTECT)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - {self.type.name} ({self.date})"

class ExerciseLog(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name='exercises')
    exercise_name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    reps = models.PositiveIntegerField()
    weight = models.FloatField()

    def __str__(self):
        return f"{self.exercise_name}: {self.sets}x{self.reps} @ {self.weight}kg"

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_logs')
    date = models.DateField()
    body_weight = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.body_weight}kg ({self.date})"