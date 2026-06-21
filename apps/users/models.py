from django.db import models
from django.contrib.auth.models import User
from datetime import date

class UserProfile(models.Model):
    GENDER_CHOICES = [('M', 'Мужской'), ('F', 'Женский')]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Аватар")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    birth_date = models.DateField(verbose_name="Дата рождения")
    height_cm = models.FloatField(verbose_name="Рост (см)")
    target_weight = models.FloatField(verbose_name="Целевой вес (кг)", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

    def __str__(self):
        return f"Профиль: {self.user.username}"