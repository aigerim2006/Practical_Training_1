from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, WorkoutForm, QuickWeightForm
from .services import FitnessService
from .models import Workout, WorkoutType
import datetime

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            UserProgress.objects.create(
                user=user, date=datetime.date.today(),
                body_weight=form.cleaned_data['initial_weight'], notes="Стартовый маркер"
            )
            login(request, user)
            messages.success(request, f"Регистрация успешна! Добро пожаловать, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Ошибка регистрации. Проверьте корректность данных.")
    else:
        form = UserRegisterForm()
    return render(request, 'fitness/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Рады видеть вас снова, {user.username}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Неверный логин или пароль.")
    else:
        form = AuthenticationForm()
    return render(request, 'fitness/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Сессия успешно завершена.")
    return redirect('login')

@login_required
def dashboard_view(request):
    analytics = FitnessService.get_dashboard_analytics(request.user)
    if request.method == 'POST':
        weight_form = QuickWeightForm(request.POST)
        if weight_form.is_valid():
            progress = weight_form.save(commit=False)
            progress.user = request.user
            progress.save()
            messages.success(request, "Антропометрические данные успешно обновлены.")
            return redirect('dashboard')
    else:
        weight_form = QuickWeightForm(initial={'date': datetime.date.today()})

    context = {**analytics, 'weight_form': weight_form}
    return render(request, 'fitness/dashboard.html', context)

@login_required
def add_workout_view(request):
    if request.method == 'POST':
        workout_form = WorkoutForm(request.POST)
        if workout_form.is_valid():
            exercises = []
            ex_names = request.POST.getlist('ex_name[]')
            ex_sets = request.POST.getlist('ex_sets[]')
            ex_reps = request.POST.getlist('ex_reps[]')
            ex_weights = request.POST.getlist('ex_weight[]')

            for i in range(len(ex_names)):
                if ex_names[i].strip():
                    exercises.append({
                        'exercise_name': ex_names[i],
                        'sets': ex_sets[i] if ex_sets[i] else 0,
                        'reps': ex_reps[i] if ex_reps[i] else 0,
                        'weight': ex_weights[i] if ex_weights[i] else 0.0,
                    })

            FitnessService.register_workout_session(
                user=request.user,
                workout_date=workout_form.cleaned_data['date'],
                workout_type=workout_form.cleaned_data['type'],
                duration=workout_form.cleaned_data['duration_minutes'],
                exercises_data=exercises
            )
            messages.success(request, "Лог тренировки успешно зафиксирован в базе данных.")
            return redirect('dashboard')
    else:
        workout_form = WorkoutForm(initial={'date': datetime.date.today()})
    return render(request, 'fitness/workout_form.html', {'workout_form': workout_form})

@login_required
def delete_workout_view(request, pk):
    """Безопасное удаление лога тренировки с контролем доступа (ТЗ п. 4.3)"""
    workout = get_object_or_404(Workout, pk=pk, user=request.user)
    if request.method == 'POST':
        workout.delete()
        messages.success(request, "Запись о тренировке успешно удалена.")
        return redirect('dashboard')
    return render(request, 'fitness/workout_confirm_delete.html', {'workout': workout})