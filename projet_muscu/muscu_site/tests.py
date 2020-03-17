import datetime

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .forms import SessionForm, ExerciseForm
from .models import TrainingSession, Exercise

class SessionCreationTest(TestCase):
    def test_date_in_future(self):
        self.response = self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': '10.01.2050',
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })

        self.assertFormError(
            self.response,
            'session_form',
            'date',
            'La date ne doit pas être dans le futur !'
        )

    def test_date_in_past(self):
        nb_instances_sessions = TrainingSession.objects.count()
        self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': datetime.date.today(),
            'exercise': 'exercice',
            'sets': 3,
            'reps': 12,
            'time_break': 60,
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })

        self.assertEqual(TrainingSession.objects.count(), nb_instances_sessions)
