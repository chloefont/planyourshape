import datetime
from django import forms
from django.forms import ValidationError
from django.forms import ModelForm
from .models import TrainingSession, Exercice

class SessionForm(ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['session_title', 'date']

        def clean_date(self, cleaned_data):
            if cleaned_data['date'] <= datetime.date.today():
                raise ValidationError("La date doit être dans le futur")
            return cleaned_data

class ExerciceForm(ModelForm):
    class Meta:
        model = Exercice
        fields = ['exercice', 'sets', 'reps', 'break_time']
