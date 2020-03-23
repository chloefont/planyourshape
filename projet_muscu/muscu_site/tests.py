from django.test import TestCase
from django.urls import reverse
from .forms import SessionForm, ExerciseForm
from .models import TrainingSession, Exercise
from .views import sessions_list

from .models import TrainingSession


class SessionListTest(TestCase):

    def test_sessions_in_list_ordered_by_time(self):
        TrainingSession.objects.create(
            session_title='recent session',
            date='2020-04-21'
        )
        TrainingSession.objects.create(
            session_title='old session',
            date='2020-03-01'
        )

        response = self.client.get(reverse('list_sessions'))
        self.assertIn('training_sessions', response.context[0])
        data = response.context['training_sessions']

        self.assertEqual(data.all()[0].session_title, 'recent session')
        self.assertEqual(data.all()[1].session_title, 'old session')


class SessionCreationTest(TestCase):

    def test_string_in_sets(self):
        self.response = self.client.post(reverse('create_session'), data={
            'session_title': 'Ma Session',
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
