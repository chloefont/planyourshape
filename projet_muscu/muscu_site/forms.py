import datetime
from django.forms import ModelForm, ValidationError, DateInput
from .models import TrainingSession, Exercise

class SessionForm(ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['session_title', 'date']

        labels = {
            'session_title': 'Titre de la séance:',
            'date': 'Date de création de la séance:',
        }
        widgets = {
            'date': DateInput(attrs={'type':'date'})
        }

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise ValidationError("La date ne doit pas être dans le futur !")
        return date

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
