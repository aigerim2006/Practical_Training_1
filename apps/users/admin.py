from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile # Обязательно импортируй

# 1. Убираем стандартного юзера из админки (если хочешь кастомный вид)
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# 2. РЕГИСТРИРУЕМ ПРОФИЛЬ (Здесь появится поле Avatar)
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_date', 'height_cm')
    # Поле avatar теперь будет доступно здесь
    fields = ('user', 'avatar', 'gender', 'birth_date', 'height_cm', 'target_weight')