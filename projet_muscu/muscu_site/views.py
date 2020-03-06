from django.shortcuts import render
from django.forms import formset_factory
from .models import TrainingSession, Exercice
from .forms import SessionForm, ExerciceForm

def session_creation(request):
    initial_nb_of_row = range(1,4)
    session_form = SessionForm(request.POST)
    ExerciceFormSet = formset_factory(ExerciceForm, extra = 3)
    data = {
        'form-TOTAL_FORMS': '3',
        'form-INITIAL_FORMS': '0',
        'form-MAX_NUM_FORMS': '10',
    }

    exercice_formset = ExerciceFormSet(data, request.POST, request.FILES)

    if session_form.is_valid() and exercice_formset.is_valid():

        TrainingSession.objects.create(
            session_title=session_form.cleaned_data['session_title'],
            date=session_form.cleaned_data['date'],
        )




    # if request.method == 'POST':
    #
    #     session = TrainingSession.create(
    #         label = request.POST.get('session_title'),
    #         date = request.POST.get('creation_date')
    #     )
    #
    #     exercices = Exercice.create(
    #         training_session = session
    #     )
    #
    #     for number in initial_nb_of_row:
    #         session.exercice.label = request.POST.get('ex' + str(number))
    #         session.exercice.sets = request.POST.get('set' + str(number))
    #         session.exercice.reps = request.POST.get('rep' + str(number))
    #         session.exercice.break_time = request.POST.get('bk' + str(number))

    context = {
        'nb_elements': initial_nb_of_row,
        'session_form': session_form,
        'exercice_formset': exercice_formset,
    }
    return render(request, 'muscu_site/session_creation.html', context)
