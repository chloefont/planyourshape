from django.forms import ModelForm, DateInput, Textarea, HiddenInput
from .models import TrainingSession, Exercise, TrainingSessionCompleted, ExerciseCompleted


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
            'exercise': "Nom de l'exercice",
            'sets': "Séries",
            'reps': "Répétitions",
            'break_time': "Temps de pause",
        }


class SessionCompletedForm(ModelForm):
    class Meta:
        model = TrainingSessionCompleted
        fields = ['date_completed']

        labels = {
            'date_completed': 'Date de la séance:',
        }

        widgets = {
            'date_completed': DateInput(attrs={'type': 'date'})
        }


class ExerciseCompletedForm(ModelForm):
    class Meta:
        model = ExerciseCompleted
        fields = ['exercise', 'weight', 'comment']

        labels = {
            'weight': 'Poids:',
            'comment': 'Commentaires:',
        }

        widgets = {
            'exercise': HiddenInput(attrs={'type': 'hidden'}),
            'comment': Textarea(attrs={'type': 'textarea', 'cols': 50, 'rows': 6}),
        }
