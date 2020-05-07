from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from .forms import (SessionForm, ExerciseForm, SessionCompletedForm,
                    ExerciseCompletedForm)
from .models import TrainingSession, Exercise, TrainingSessionCompleted, ExerciseCompleted


def sessions_list(request):
    training_sessions = TrainingSession.objects.filter(visible=True).order_by('-date')
    training_sessions_completed = TrainingSessionCompleted.objects.order_by('-date_completed')
    context = {
        'training_sessions': training_sessions,
        'training_sessions_completed': training_sessions_completed,
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

            return redirect('sessions_list')

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
    exercises = training_session.exercises.all()
    number_exercises = len(exercises)
    ExerciseCompletedFormSet = formset_factory(ExerciseCompletedForm,
                                               extra=number_exercises)
    list_exercice_form = []

    if request.method == 'POST':
        session_completed_form = SessionCompletedForm(request.POST)
        exercise_completed_formset = ExerciseCompletedFormSet(request.POST)

        if session_completed_form.is_valid() and exercise_completed_formset.is_valid():
            session_completed = TrainingSessionCompleted.objects.create(
                training_session=training_session,
                date_completed=session_completed_form.cleaned_data['date_completed'],
            )

            number_ex = 0
            for exercise_completed_form in exercise_completed_formset:
                if exercise_completed_form.cleaned_data:
                    ExerciseCompleted.objects.create(
                        training_session_completed=session_completed,
                        exercise=exercises[number_ex],
                        weight=exercise_completed_form.cleaned_data['weight'],
                        comment=exercise_completed_form.cleaned_data['comment'],
                    )
                    number_ex += 1

                return redirect('sessions_list')

    else:
        session_completed_form = SessionCompletedForm()
        exercise_completed_formset = ExerciseCompletedFormSet()

    ex_position = 0
    for exercise in exercises:
        list_exercice_form.append((exercise,
                                  exercise_completed_formset[ex_position]))
        ex_position += 1

    context = {
        'training_session': training_session,
        'session_completed_form': session_completed_form,
        'exercise_completed_formset': exercise_completed_formset,
        'list_exercice_form': list_exercice_form,
    }

    return render(request, 'muscu_site/session_complete.html', context)


def delete_session(request, session_id):
    training_session = get_object_or_404(TrainingSession, id=session_id)
    exercises = Exercise.objects.all().filter(
        training_session=training_session
    )

    if request.method == 'POST':
        if training_session.session_completed:
            training_session.visible = False
            training_session.save()
        else:
            training_session.delete()
        return redirect('sessions_list')

    context = {
        'training_session': training_session,
        'exercises': exercises,
    }

    return render(request, 'muscu_site/session_delete_confirmation.html', context)
