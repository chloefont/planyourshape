from django.shortcuts import render
from .models import TrainingSession, Exercice
from .forms import SessionForm

def session_creation(request):
    initial_nb_of_row = range(1,4)
    session_form = SessionForm(request.POST)

    if session_form.is_valid():

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
        'form': session_form,
    }
    return render(request, 'muscu_site/session_creation.html', context)
