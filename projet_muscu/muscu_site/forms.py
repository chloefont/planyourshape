from django.forms import ModelForm
from .models import TrainingSession, Exercise

from datetime import datetime


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

        labels = {
            'exercise': 'Exercice',
            'sets': 'Séries',
            'reps': 'Répétitions',
            'break_time': 'Temps de pause',
        }


class SessionCompletedForm(ModelForm):
    class Meta:
        model = TrainingSessionCompleted
        fields = ['date_completed']
        use_required_attribute = False

        labels = {
            'date_completed': 'Date de la séance:',
        }

        widgets = {
            'date_completed': DateInput(attrs={'type': 'date', 'required': False}),
        }


class ExerciseCompletedForm(ModelForm):
    class Meta:
        model = ExerciseCompleted
        fields = ['weight', 'comment']

        labels = {
            'weight': 'Poids:',
            'comment': 'Commentaires:',
        }

        widgets = {
            'weight': NumberInput(attrs={'required': False}),
            'comment': Textarea(attrs={'type': 'textarea', 'cols': 50, 'rows': 6}),
        }
