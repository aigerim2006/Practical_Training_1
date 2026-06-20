from django import forms
from .models import UserProgress
from apps.users.forms import TailwindFormMixin

class UserProgressForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'body_weight', 'notes']
        widgets = {
            'date': forms.DateInput(
                attrs={
                    'type': 'date', 
                    'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm'
                }
            ),
            'body_weight': forms.NumberInput(
                attrs={
                    'step': '0.1', 
                    'placeholder': 'Напр. 70.5',
                    'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3, 
                    'placeholder': 'Самочувствие или замеры...',
                    'class': 'w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm'
                }
            ),
        }