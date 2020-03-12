from django.shortcuts import render
from django.forms import formset_factory
from .forms import SessionForm, ExerciceForm
from .models import TrainingSession, Exercice

def session_creation(request):
    ExerciceFormSet = formset_factory(ExerciceForm, extra = 3)
    data = {
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '10',
    }
    if request.method == 'POST':
        session_form = SessionForm(request.POST)
        exercice_formset = ExerciceFormSet(request.POST, request.FILES)

        if session_form.is_valid() and exercice_formset.is_valid():


            session = TrainingSession.objects.create(
                session_title=session_form.cleaned_data['session_title'],
                date=session_form.cleaned_data['date'],
            )


            for ex in exercice_formset.forms:
                if ex.cleaned_data:
                    Exercice.objects.create(
                        training_session = session,
                        exercice = ex.cleaned_data['exercice'],
                        sets = ex.cleaned_data['sets'],
                        reps = ex.cleaned_data['reps'],
                        break_time = ex.cleaned_data['break_time'],
                    )
    else:
        session_form = SessionForm();
        exercice_formset = ExerciceFormSet()

    context = {
        'session_form': session_form,
        'exercice_formset': exercice_formset,
    }
    return render(request, 'muscu_site/session_creation.html', context)
