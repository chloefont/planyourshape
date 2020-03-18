from django.shortcuts import render, redirect
from django.forms import formset_factory
from .forms import SessionForm, ExerciseForm
from .models import TrainingSession, Exercise

def create_session(request):
    ExerciseFormSet = formset_factory(ExerciseForm, extra = 3)
    if request.method == 'POST':
        session_form = SessionForm(request.POST)
        exercise_formset = ExerciseFormSet(request.POST)

        if session_form.is_valid() and exercise_formset.is_valid():

            session = TrainingSession.objects.create(
                session_title=session_form.cleaned_data['session_title'],
                date=session_form.cleaned_data['date'],
            )


            for ex in exercise_formset.forms:
                if ex.cleaned_data:
                    Exercise.objects.create(
                        training_session = session,
                        exercise = ex.cleaned_data['exercise'],
                        sets = ex.cleaned_data['sets'],
                        reps = ex.cleaned_data['reps'],
                        break_time = ex.cleaned_data['break_time'],
                    )
            return redirect('create_session')
    else:
        session_form = SessionForm();
        exercise_formset = ExerciseFormSet()

    context = {
        'session_form': session_form,
        'exercise_formset': exercise_formset,
    }
    return render(request, 'muscu_site/session_creation.html', context)
