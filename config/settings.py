from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-lnrkjnhopo+bld_t*n18*vchnbu3ovi%8)zd43sgs&x6yo_v2h'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.users',
    'apps.workouts',
    'apps.analytics',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ИСПРАВЛЕНО: было core.wsgi
WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ru-ru' # Изменил на русский
TIME_ZONE = 'Asia/Bishkek'
USE_I18N = True
USE_TZ = True

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'analytics:dashboard'
LOGOUT_REDIRECT_URL = 'users:login'

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "site_title": "Администрирование фитнес-проекта",
    "site_header": "Фитнес-трекер",
    "site_brand": "Управление",
    "welcome_sign": "Добро пожаловать в админ-панель!",
    "copyright": "Fitness Project Ltd",
    
    # Иконки для меню
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "apps.Workout": "fas fa-dumbbell",  # Замените на ваши пути к моделям
        "apps.Exercise": "fas fa-running",
        "apps.UserProgress": "fas fa-chart-line",
    },

    "show_sidebar": True,
    "navigation_expanded": True,
    "order_with_respect_to": ["auth", "apps.Workout", "apps.Exercise", "apps.UserProgress"],
    
    # Убираем лишние стандартные группы, если нужно
    "hide_apps": [], 
}

JAZZMIN_UI_TWEAKS = {
    # Светлая тема, как на изображении
    "theme": "default",  
    
    # Настройки цветовых схем для элементов
    "navbar": "navbar-white navbar-light",  # Белая верхняя панель
    "sidebar": "sidebar-light-primary",     # Светлая боковая панель с синим акцентом
    "sidebar_fixed": True,
    "sidebar_nav_child_indent": True,
    
    # Настройка логотипа и фона
    "brand_colour": "navbar-primary",
    "accent": "accent-primary",
    
    # Настройка кнопок (зеленые кнопки Add/Change)
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}