from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Workout, ExerciseLog, WorkoutType, WorkoutSchedule
from .forms import WorkoutForm, WorkoutScheduleForm
from apps.analytics.models import UserProgress
import datetime
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'
    paginate_by = 10

    def get_queryset(self):
        # Базовый запрос
        queryset = Workout.objects.filter(user=self.request.user).select_related('type')
        
        # Получаем ID типа из параметров URL (?type=1)
        type_id = self.request.GET.get('type')
        if type_id:
            queryset = queryset.filter(type_id=type_id)
            
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем все типы тренировок для кнопок-фильтров
        context['workout_types'] = WorkoutType.objects.all()
        # Передаем активный фильтр, чтобы подсветить нужную кнопку
        context['active_type'] = self.request.GET.get('type', '')
        return context

class WorkoutDetailView(LoginRequiredMixin, DetailView):
    model = Workout
    template_name = 'workouts/workout_detail.html'
    context_object_name = 'workout'

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).prefetch_related('exercises')

class AddWorkoutView(LoginRequiredMixin, View):
    def get(self, request):
        form = WorkoutForm(initial={'date': datetime.date.today()})
        return render(request, 'workouts/workout_form.html', {'form': form})

    def post(self, request):
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            
            # Расчет калорий
            latest_weight_log = UserProgress.objects.filter(user=request.user, date__lte=workout.date).order_by('-date').first()
            weight = latest_weight_log.body_weight if latest_weight_log else 70.0
            
            # workout.type теперь берется из формы корректно
            met = workout.type.met_coefficient
            workout.calories_burned = round(float(met * 3.5 * weight / 200.0 * workout.duration_minutes), 1)
            workout.save()

            # Обработка упражнений
            names = request.POST.getlist('ex_name[]')
            sets = request.POST.getlist('ex_sets[]')
            reps = request.POST.getlist('ex_reps[]')
            weights = request.POST.getlist('ex_weight[]')

            for i in range(len(names)):
                if names[i].strip():
                    ExerciseLog.objects.create(
                        workout=workout, 
                        exercise_name=names[i].strip(),
                        sets=int(sets[i] or 0), 
                        reps=int(reps[i] or 0), 
                        weight=float(weights[i] or 0)
                    )
            return redirect('workouts:workout_list')
        
        # Если форма невалидна, она будет возвращена с ошибками и списком типов
        return render(request, 'workouts/workout_form.html', {'form': form})

class DeleteWorkoutView(LoginRequiredMixin, View):
    def post(self, request, pk):
        workout = get_object_or_404(Workout, pk=pk, user=request.user)
        workout.delete()
        return redirect('workouts:workout_list')
    
class ScheduleView(LoginRequiredMixin, ListView):
    model = WorkoutSchedule
    template_name = 'workouts/schedule.html'
    context_object_name = 'schedule_items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Подготавливаем список дней недели прямо здесь
        context['days_of_week'] = [
            (0, 'Понедельник'), (1, 'Вторник'), (2, 'Среда'), 
            (3, 'Четверг'), (4, 'Пятница'), (5, 'Суббота'), (6, 'Воскресенье')
        ]
        return context
    
class DeleteScheduleView(LoginRequiredMixin, View):
    def get(self, request, pk):
        schedule = get_object_or_404(WorkoutSchedule, pk=pk, user=request.user)
        return render(request, 'workouts/confirm_delete_schedule.html', {'schedule': schedule})

    def post(self, request, pk):
        schedule = get_object_or_404(WorkoutSchedule, pk=pk, user=request.user)
        schedule.delete()
        return redirect('workouts:schedule')

@login_required
def add_schedule_view(request):
    if request.method == 'POST':
        form = WorkoutScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.user = request.user
            schedule.save()
            return redirect('workouts:schedule')
    else:
        form = WorkoutScheduleForm()
    return render(request, 'workouts/add_schedule.html', {'form': form})

@login_required
@require_POST
def delete_schedule_view(request, pk):
    schedule = get_object_or_404(WorkoutSchedule, pk=pk, user=request.user)
    schedule.delete()
    return redirect('workouts:schedule')

class UpdateScheduleView(LoginRequiredMixin, UpdateView):
    model = WorkoutSchedule
    form_class = WorkoutScheduleForm
    template_name = 'workouts/add_schedule.html' # Используем тот же шаблон, что и для добавления
    success_url = '/workouts/schedule/'

    def get_queryset(self):
        return WorkoutSchedule.objects.filter(user=self.request.user)