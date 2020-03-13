import datetime
from django.forms import ModelForm, ValidationError
from .models import TrainingSession, Exercise

class SessionForm(ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['session_title', 'date']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today():
            raise ValidationError("La date ne doit pas être dans le futur !")
        return date

class ExerciseForm(ModelForm):
    class Meta:
        model = Exercise
        fields = ['exercise', 'sets', 'reps', 'break_time']
