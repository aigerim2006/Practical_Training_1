from django import forms
from django.contrib.auth.models import User
from .models import Workout, UserProgress

class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    initial_weight = forms.FloatField(required=True, label="Текущий вес тела (кг)")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с такой почтой уже существует.")
        return email

    def clean_initial_weight(self):
        weight = self.cleaned_data.get('initial_weight')
        if weight <= 0:
            raise forms.ValidationError("Вес должен быть строго больше нуля.")
        return weight

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'type', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Минут'}),
        }

    def clean_duration_minutes(self):
        duration = self.cleaned_data.get('duration_minutes')
        if duration <= 0:
            raise forms.ValidationError("Продолжительность должна быть больше нуля.")
        return duration

class QuickWeightForm(forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'body_weight', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'body_weight': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_body_weight(self):
        weight = self.cleaned_data.get('body_weight')
        if weight <= 0:
            raise forms.ValidationError("Вес не может быть отрицательным или нулевым.")
        return weight