from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from .forms import (SessionForm, ExerciseForm, SessionCompletedForm,
                    ExerciseCompletedForm)
from .models import TrainingSession, Exercise, TrainingSessionCompleted


def signup(request) :
    if request.method == 'POST' :
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('sessions_list')
    else :
        context = {
            'signup_form' : UserCreationForm(),
        }

    return render(request, 'muscu_site/signup.html', context)

@login_required
def sessions_list(request):
    training_sessions = request.user.training_session.filter(visible=True).order_by('-date')
    training_sessions_completed = request.user.training_session_completed.all().order_by('-date_completed').select_related('training_session')
    context = {
        'training_sessions': training_sessions,
        'training_sessions_completed': training_sessions_completed,
        'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
    }

    return render(request, 'muscu_site/sessions_list.html', context)


@login_required
def create_session(request):
    ExerciseFormSet = formset_factory(ExerciseForm, extra=3)
    if request.method == 'POST' and request.user.has_perm('muscu_site.training_session.can_add_training_session'):
        session_form = SessionForm(request.POST)
        exercise_formset = ExerciseFormSet(request.POST)

        if session_form.is_valid() and exercise_formset.is_valid():

            session = TrainingSession.objects.create(
                user_id=request.user.id,
                session_title=session_form.cleaned_data['session_title'],
            )
            request.user.training_session.add(session)

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
        'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
    }
    return render(request, 'muscu_site/session_creation.html', context)


@login_required
@transaction.atomic
def complete_session(request, session_id):
    training_session = get_object_or_404(TrainingSession, id=session_id)

    if training_session in request.user.training_session.filter(visible=True) :
        exercises = training_session.exercises.all()
        ExerciseCompletedFormSet = formset_factory(ExerciseCompletedForm, extra=0)

        if request.method == 'POST' and request.user.has_perm(
            'muscu_site.training_session_completed.can_add_training_session_completed'
        ):
            session_completed_form = SessionCompletedForm(request.POST)
            exercise_completed_formset = ExerciseCompletedFormSet(request.POST)

            if session_completed_form.is_valid() and exercise_completed_formset.is_valid():
                session_completed = session_completed_form.save(commit=False)
                session_completed.training_session = training_session
                session_completed.save()
                request.user.training_session_completed.add(session_completed)

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
            'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
        }

        return render(request, 'muscu_site/session_complete.html', context)

    else :
        return redirect('sessions_list')


@login_required
def session_summary(request, session_completed_id):
    training_session_completed = get_object_or_404(TrainingSessionCompleted, id=session_completed_id)

    if training_session_completed in request.user.training_session_completed.all() :
        exercises_completed = training_session_completed.exercises_completed.all()

        context = {
            'training_session_completed': training_session_completed,
            'exercises_completed': exercises_completed,
            'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
        }
        return render(request, 'muscu_site/session_summary.html', context)

    else :
        return redirect('sessions_list')

@login_required
def delete_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id)

    if session in request.user.training_session.filter(visible=True) :
        if request.method == 'POST' and request.user.has_perm('muscu_site.training_session.can_delete_training_session'):
            if session.sessions_completed:
                session.visible = False
                session.save()
            else:
                session.delete()
            return redirect('sessions_list')

        context = {
            'session': session,
            'session_title': session.session_title,
            'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
        }

        return render(request, 'muscu_site/session_delete_confirmation.html', context)

    else :
        return redirect('sessions_list')


@login_required
def delete_session_completed(request, session_completed_id):
    session_completed = get_object_or_404(TrainingSessionCompleted, id=session_completed_id)

    if session_completed in request.user.training_session_completed.all() :
        if request.method == 'POST' and request.user.has_perm('muscu_site.can_delete_training_session_completed'):
            session_completed.delete()
            return redirect('sessions_list')

        context = {
            'session_completed': session_completed,
            'session_title': session_completed.training_session.session_title,
            'hasnt_all_perms': not request.user.has_perm('muscu_site.training_session.can_add_training_session'),
        }

        return render(request, 'muscu_site/session_completed_delete_confirmation.html', context)

    else :
        return redirect('sessions_list')
