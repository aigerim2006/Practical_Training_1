from django.db import models
from django.contrib.auth.models import User

class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    date = models.DateField()
    body_weight = models.FloatField()
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Прогресс пользователя'
        verbose_name_plural = 'Прогресс пользователей'
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.date} ({self.body_weight}kg)"