from django.shortcuts import render

def session_creation(request):
    initial_nb_of_row = range(1,4)

    if request.method == 'POST':
        if 'exercices' not in request.session:
            request.session['execices'] = {}

    context = {
        'nb_elements': initial_nb_of_row,
    }
    return render(request, 'muscu_site/session_creation.html', context)
