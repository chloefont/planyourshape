import datetime

from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TrainingSession(models.Model):
    session_title = models.CharField(max_length=100)
    date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.session_title

class Exercice(models.Model):
    training_session = models.ForeignKey(
        TrainingSession, on_delete=models.CASCADE, related_name='exercice'
    )
    exercice = models.CharField(max_length=100, blank=True)
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(default=1)
    break_time = models.IntegerField(default=60)

    def __str__(self):
        return self.exercice

class SessionForm(ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['session_title', 'date']
        labels = {
            'session_title': _('Titre de la séance'),
        }

        help_texts = {
            'session_title': _('Titre de la séance')
        }

        error_messages = {
            'session_title': {
                'max_length': _('Le titre de cette séance est trop long.')
            }
        }


class ExerciceForm(ModelForm):
    class Meta:
        model = Exercice
        fields = ['exercice', 'sets', 'reps', 'break_time']
