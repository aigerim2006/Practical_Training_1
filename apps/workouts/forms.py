from django import forms
from .models import Workout
from apps.users.forms import TailwindFormMixin

class WorkoutForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'type', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'}),
            'type': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'}),
            'duration_minutes': forms.NumberInput(attrs={'placeholder': 'Мин', 'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'}),
        }
