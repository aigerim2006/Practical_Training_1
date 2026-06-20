from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm
from .models import UserProfile # Импорт лучше делать сверху
from apps.analytics.models import UserProgress
import datetime

class RegisterView(View):
    def get(self, request):
        return render(request, 'users/register.html', {'form': UserRegisterForm()})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            UserProfile.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                birth_date=form.cleaned_data['birth_date'],
                height_cm=form.cleaned_data['height_cm']
            )
            
            UserProgress.objects.create(
                user=user,
                date=datetime.date.today(),
                body_weight=form.cleaned_data['initial_weight'],
                notes="Стартовый маркер при регистрации"
            )
            login(request, user)
            return redirect('analytics:dashboard')
        return render(request, 'users/register.html', {'form': form})

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        # Добавлена проверка, есть ли профиль
        profile = getattr(request.user, 'profile', None) 
        latest_weight = UserProgress.objects.filter(user=request.user).order_by('-date').first()
        
        weight = latest_weight.body_weight if latest_weight else 70.0
        # Если профиля нет, ставим дефолтные значения, чтобы не было ошибки
        bmr = 0
        if profile:
            age = profile.get_age()
            bmr = (10 * weight) + (6.25 * profile.height_cm) - (5 * age)
            bmr = bmr + 5 if profile.gender == 'M' else bmr - 161

        context = {'profile': profile, 'current_weight': weight, 'bmr': round(bmr, 1)}
        return render(request, 'users/profile.html', context)