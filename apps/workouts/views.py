from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Workout, ExerciseLog, WorkoutType
from .forms import WorkoutForm
from apps.analytics.models import UserProgress
import datetime

class WorkoutListView(LoginRequiredMixin, ListView):
    model = Workout
    template_name = 'workouts/workout_list.html'
    context_object_name = 'workouts'
    paginate_by = 10

    def get_queryset(self):
        return Workout.objects.filter(user=self.request.user).select_related('type')

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