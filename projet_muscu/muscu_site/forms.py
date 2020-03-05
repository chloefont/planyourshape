from django import forms
from muscu_site.models import TrainingSession
from django.utils import timezone


class SessionForm(forms.Form):
    session_title = forms.CharField(label='Titre de la séance', max_length=100, required=True)
    date = forms.DateField(label='Date de création', required=False)
