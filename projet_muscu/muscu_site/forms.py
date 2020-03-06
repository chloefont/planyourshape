from django import forms
from django.forms import formset_factory
from muscu_site.models import TrainingSession, Exercice
from django.utils import timezone


class SessionForm(forms.Form):
    session_title = forms.CharField(label='Titre de la séance', max_length=100, required=True)
    date = forms.DateField(label='Date de création', required=False)

class ExerciceForm(forms.Form):
    exercice = forms.CharField(max_length=100)
    sets = forms.IntegerField()
    reps = forms.IntegerField()
    break_time = forms.IntegerField()
