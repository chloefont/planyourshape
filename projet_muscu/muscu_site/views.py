from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .forms import SessionForm, ExerciseForm, SessionCompletedForm, ExerciseCompletedForm
from .models import TrainingSession, Exercise


def list_sessions(request):
    training_sessions = TrainingSession.objects.order_by('-date')
    context = {
        'training_sessions': training_sessions,
    }

    return render(request, 'muscu_site/sessions_list.html', context)


def create_session(request):
    ExerciseFormSet = formset_factory(ExerciseForm, extra=3)
    if request.method == 'POST':
        session_form = SessionForm(request.POST)
        exercise_formset = ExerciseFormSet(request.POST)

        if session_form.is_valid() and exercise_formset.is_valid():

            session = TrainingSession.objects.create(
                session_title=session_form.cleaned_data['session_title'],
            )

            for ex in exercise_formset.forms:
                if ex.cleaned_data:
                    Exercise.objects.create(
                        training_session=session,
                        exercise=ex.cleaned_data['exercise'],
                        sets=ex.cleaned_data['sets'],
                        reps=ex.cleaned_data['reps'],
                        break_time=ex.cleaned_data['break_time'],
                    )

            return redirect('list_sessions')

    else:
        session_form = SessionForm()
        exercise_formset = ExerciseFormSet()

    context = {
        'session_form': session_form,
        'exercise_formset': exercise_formset,
    }
    return render(request, 'muscu_site/session_creation.html', context)

def complete_session(request, session_id):
    training_session = get_object_or_404(TrainingSession, id=session_id)
    exercises = Exercise.objects.all().filter(training_session=training_session)

    context = {
        'training_session': training_session,
        'exercises': exercises,
    }

    return render(request, 'muscu_site/session_complete.html', context)
