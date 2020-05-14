from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.db import transaction
from .forms import (SessionForm, ExerciseForm, SessionCompletedForm,
                    ExerciseCompletedForm)
from .models import TrainingSession, Exercise, TrainingSessionCompleted


def sessions_list(request):
    training_sessions = TrainingSession.objects.filter(visible=True).order_by('-date')
    training_sessions_completed = TrainingSessionCompleted.objects.order_by('-date_completed').select_related('training_session')
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


@transaction.atomic
def complete_session(request, session_id):
    training_session = get_object_or_404(TrainingSession, id=session_id)
    exercises = training_session.exercises.all()
    ExerciseCompletedFormSet = formset_factory(ExerciseCompletedForm, extra=0)

    if request.method == 'POST':
        session_completed_form = SessionCompletedForm(request.POST)
        exercise_completed_formset = ExerciseCompletedFormSet(request.POST)

        if session_completed_form.is_valid() and exercise_completed_formset.is_valid():
            session_completed = session_completed_form.save(commit=False)
            session_completed.training_session = training_session
            session_completed.save()
            for exercise_completed_form in exercise_completed_formset:
                exercise_completed = exercise_completed_form.save(commit=False)
                exercise_completed.training_session_completed = session_completed
                exercise_completed.save()

            return redirect('sessions_list')

    else:
        session_completed_form = SessionCompletedForm()
        exercise_completed_formset = ExerciseCompletedFormSet(initial=[
            {'exercise': exercise.id} for exercise in exercises
        ])

    list_exercise_form = zip(exercises, exercise_completed_formset)

    context = {
        'training_session': training_session,
        'session_completed_form': session_completed_form,
        'exercise_completed_formset': exercise_completed_formset,
        'list_exercise_form': list_exercise_form,
    }

    return render(request, 'muscu_site/session_complete.html', context)


def session_summary(request, session_completed_id):
    training_session_completed = get_object_or_404(TrainingSessionCompleted, id=session_completed_id)
    exercises_completed = training_session_completed.exercises_completed.all()

    context = {
        'training_session_completed': training_session_completed,
        'exercises_completed': exercises_completed
    }
    return render(request, 'muscu_site/session_summary.html', context)


def delete_session(request, session_type, session_id):
    if session_type == 'planned':
        session = get_object_or_404(TrainingSession, id=session_id)
        session_type_sentence = {
            'name': "séance",
            'session_title': session.session_title,
            'list_title': "séances planifiées",
            'explanation': "Vous ne pourrez plus compléter cette séance."
        }
        url_name = 'complete_session'

    elif session_type == 'completed':
        session = get_object_or_404(TrainingSessionCompleted, id=session_id)
        session_type_sentence = {
            'name': "séance complétée",
            'session_title': session.training_session.session_title,
            'list_title': "séances complétées",
            'explanation': "Vous n'aurez plus accès au résumé de cette séance."
        }
        url_name = 'session_summary'

    if request.method == 'POST':
        if session_type == 'planned' and session.session_completed:
            session.visible = False
            session.save()
        else:
            session.delete()
        return redirect('sessions_list')

    context = {
        'training_session': session,
        'session_type_sentence': session_type_sentence,
        'url_name': url_name,
    }

    return render(request, 'muscu_site/session_delete_confirmation.html', context)
