from django import forms
from .models import UserProgress
from apps.users.forms import TailwindFormMixin

class ProgressForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = UserProgress
        fields = ['date', 'body_weight', 'notes']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}