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
        self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': datetime.date.today(),
            'form-0-exercise': 'exercice',
            'form-0-sets': 3,
            'form-0-reps': 12,
            'form-0-break_time': 60,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })

        self.assertEqual(TrainingSession.objects.count(), 1)
        self.assertEqual(Exercise.objects.count(), 1)

    def test_string_in_sets(self):
        self.response = self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': datetime.date.today(),
            'form-0-exercise': 'exercice',
            'form-0-sets': 'sets',
            'form-0-reps': 12,
            'form-0-break_time': 60,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })


        self.assertFormsetError(
            self.response,
            'exercise_formset',
            0,
            'sets',
            'Saisissez un nombre entier.'
        )

    def test_string_in_reps(self):
        self.response = self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': datetime.date.today(),
            'form-0-exercise': 'exercice',
            'form-0-sets': 3,
            'form-0-reps': 'reps',
            'form-0-break_time': 60,
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })

        self.assertFormsetError(
            self.response,
            'exercise_formset',
            0,
            'reps',
            'Saisissez un nombre entier.'
        )

    def test_string_in_break_time(self):
        self.response = self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
            'date': datetime.date.today(),
            'form-0-exercise': 'exercice',
            'form-0-sets': 3,
            'form-0-reps': 12,
            'form-0-break_time': 'break time',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })

        self.assertFormsetError(
            self.response,
            'exercise_formset',
            0,
            'break_time',
            'Saisissez un nombre entier.'
        )
