from django import forms
from datetime import date
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from .models import UserProfile

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            })

class UserRegisterForm(TailwindFormMixin, forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    gender = forms.ChoiceField(choices=UserProfile.GENDER_CHOICES, label="Пол")
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}), 
        label="Дата рождения"
    )

    # Добавляем валидаторы для роста и веса
    height_cm = forms.FloatField(
        label="Рост (см)", 
        validators=[MinValueValidator(50.0), MaxValueValidator(250.0)]
    )
    initial_weight = forms.FloatField(
        label="Текущий вес (кг)", 
        validators=[MinValueValidator(30.0), MaxValueValidator(300.0)]
    )

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        
        # Расчет возраста
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        
        # Ограничения: например, от 14 до 90 лет
        if age < 14:
            raise forms.ValidationError("Регистрация разрешена с 14 лет.")
        if age > 90:
            raise forms.ValidationError("Пожалуйста, укажите корректную дату рождения.")
            
        return birth_date

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        pwd = self.cleaned_data.get('password')
        if len(pwd) < 8:
            raise forms.ValidationError("Пароль должен содержать минимум 8 символов.")
        return pwd
    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 14 or age > 90:
            raise forms.ValidationError("Регистрация разрешена с 14 до 90 лет.")
        return birth_date