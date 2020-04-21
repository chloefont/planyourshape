from django.forms import ModelForm
from .models import TrainingSession, Exercise


class SessionForm(ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['session_title']

        labels = {
            'session_title': 'Titre de la séance:',
        }


class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise', 'sets', 'reps', 'break_time']

        label = {
            'exercise': 'Exercice',
            'sets': 'Séries',
            'reps': 'Répétitions',
            'break_time': 'Temps de pause',
        }
