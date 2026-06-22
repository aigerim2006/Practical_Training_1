from django import forms
from .models import UserProgress
from apps.users.forms import TailwindFormMixin

class UserProgressForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'body_weight', 'notes']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date', 
                    'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm text-white placeholder-white/30'
                }
            ),
            'body_weight': forms.NumberInput(
                attrs={
                    'step': '0.1', 
                    'placeholder': 'Напр. 70.5',
                    'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm text-white placeholder-white/30'
                }
            ),
            'notes': forms.Textarea(
                attrs={
                    'rows': 3, 
                    'placeholder': 'Самочувствие или замеры...',
                    'class': 'w-full px-4 py-3 bg-white/5 border border-white/10 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none text-sm text-white placeholder-white/30'
                }
            ),
        }