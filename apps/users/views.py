from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages 
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm 
from .models import UserProfile
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
    def get_context_data(self, request, u_form=None, p_form=None):
        profile = getattr(request.user, 'profile', None)
        latest_weight = UserProgress.objects.filter(user=request.user).order_by('-date').first()
        weight = latest_weight.body_weight if latest_weight else 0.0
        
        bmr = 0
        bmi = 0
        bmi_status = "Нет данных"
        bmi_color = "text-white/40"

        if profile and weight > 0:
            # Расчет BMR
            age = profile.get_age()
            bmr = (10 * weight) + (6.25 * profile.height_cm) - (5 * age)
            bmr = bmr + 5 if profile.gender == 'M' else bmr - 161
            
            # Расчет ИМТ (BMI)
            height_m = profile.height_cm / 100
            bmi = weight / (height_m * height_m)
            
            if bmi < 18.5:
                bmi_status = "Дефицит массы"
                bmi_color = "text-blue-400"
            elif 18.5 <= bmi < 25:
                bmi_status = "Норма"
                bmi_color = "text-emerald-400"
            elif 25 <= bmi < 30:
                bmi_status = "Избыточный вес"
                bmi_color = "text-amber-400"
            else:
                bmi_status = "Ожирение"
                bmi_color = "text-rose-400"

        return {
            'profile': profile,
            'current_weight': round(weight, 1),
            'bmr': round(bmr),
            'bmi': round(bmi, 1),
            'bmi_status': bmi_status,
            'bmi_color': bmi_color,
            'u_form': u_form or UserUpdateForm(instance=request.user),
            'p_form': p_form or (ProfileUpdateForm(instance=profile) if profile else None)
        }

    def get(self, request):
        return render(request, 'users/profile.html', self.get_context_data(request))

    def post(self, request):
        profile = getattr(request.user, 'profile', None)
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=profile) if profile else None

        if u_form.is_valid() and (not p_form or p_form.is_valid()):
            u_form.save()
            if p_form:
                p_form.save()
            messages.success(request, 'Ваш профиль был успешно обновлен! 🔥')
            return redirect('users:profile')
        
        messages.error(request, 'Ой! Проверьте правильность введенных данных.')
        return render(request, 'users/profile.html', self.get_context_data(request, u_form, p_form))