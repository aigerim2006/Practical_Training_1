from django import forms
from .models import Workout, WorkoutSchedule
from apps.users.forms import TailwindFormMixin

class WorkoutForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'type', 'duration_minutes']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d', 
                attrs={
                    'type': 'date', 
                    'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'
                }
            ),
            'type': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'}),
            'duration_minutes': forms.NumberInput(attrs={'placeholder': 'Мин', 'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl'}),
        }

class WorkoutScheduleForm(forms.ModelForm):
    class Meta:
        model = WorkoutSchedule
        fields = ['day_of_week', 'exercise_name', 'time']
        widgets = {
            'day_of_week': forms.Select(attrs={'class': 'w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white'}),
            'exercise_name': forms.TextInput(attrs={'class': 'w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white', 'placeholder': 'Например: Жим лежа'}),
            'time': forms.TimeInput(attrs={'class': 'w-full p-3 bg-white/5 border border-white/10 rounded-xl text-white', 'type': 'time'}),
        }
