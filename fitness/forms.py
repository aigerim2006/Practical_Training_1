from django import forms
from django.contrib.auth.models import User
from .models import Workout, UserProgress

class TailwindFormMixin:
    """Миксин для автоматического внедрения стилей Tailwind во все поля формы"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-4 py-2.5 bg-gray-50 border border-gray-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition text-sm'
            })

class UserRegisterForm(TailwindFormMixin, forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    initial_weight = forms.FloatField(required=True, label="Текущий вес тела (кг)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Пароль должен содержать не менее 8 символов (Требование безопасности ТЗ).")
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return email

    def clean_initial_weight(self):
        weight = self.cleaned_data.get('initial_weight')
        if weight <= 30 or weight > 250:
            raise forms.ValidationError("Введите реалистичное значение веса (от 30 до 250 кг).")
        return weight

class WorkoutForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'type', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')
        if duration <= 0 or duration > 480:
            raise forms.ValidationError("Длительность тренировки должна быть от 1 до 480 минут.")
        return duration

class QuickWeightForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'body_weight', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.TextInput(attrs={'placeholder': 'Самочувствие, цели...'}),
        }

    def clean_body_weight(self):
        weight = self.cleaned_data.get('body_weight')
        if weight <= 30:
            raise forms.ValidationError("Вес должен быть физически реалистичным и больше 30 кг.")
        return weight