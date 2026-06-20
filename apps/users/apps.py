from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Пишем полный путь через точку, иначе Django потеряет приложение
    name = 'apps.users' 
    # Красивое отображение в админ-панели
    verbose_name = 'Управление пользователями и физиологией'
