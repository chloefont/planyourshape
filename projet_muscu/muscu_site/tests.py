from django.test import TestCase
from django.urls import reverse

from muscu_site.models import TrainingSession, Exercise, TrainingSessionCompleted


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

        response = self.client.get(reverse('sessions_list'))
        self.assertIn('training_sessions', response.context[0])
        data = response.context['training_sessions']

        self.assertEqual(data.all()[0].session_title, 'recent session')
        self.assertEqual(data.all()[1].session_title, 'old session')


class SessionCreationTest(TestCase):

    def test_string_in_sets(self):
        response = self.client.post(reverse('create_session'), data={
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
            response,
            'exercise_formset',
            0,
            'sets',
            'Saisissez un nombre entier.'
        )

    def test_string_in_reps(self):
        response = self.client.post(reverse('create_session'), data={
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
            response,
            'exercise_formset',
            0,
            'reps',
            'Saisissez un nombre entier.'
        )

    def test_string_in_break_time(self):
        response = self.client.post(reverse('create_session'), data={
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
            response,
            'exercise_formset',
            0,
            'break_time',
            'Saisissez un nombre entier.'
        )


class SessionCompleteTest(TestCase):

    def setUp(self):
        self.training_session = TrainingSession.objects.create(
            session_title='Ma Session',
            date='2020-01-01'
        )
        Exercise.objects.create(
            exercise='Exercice',
            training_session=self.training_session
        )

    def test_register_session_completed_with_date_creates_object(self):
        self.client.post(reverse('complete_session', kwargs={'session_id': self.training_session.id}), data={
            'date_completed': '2020-04-03',
            'form-0-exercise': self.training_session.exercises.first().id,
            'form-0-weight': 10,
            'form-0-comment': 'commentaire qualitatif',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '1',
            'form_MAX_FORMS': '1000',
        })

        session_completed = TrainingSessionCompleted.objects.filter(date_completed='2020-04-03').first()

        self.assertEqual(TrainingSessionCompleted.objects.filter(date_completed='2020-04-03').count(), 1)
        self.assertTrue(session_completed, "No TrainingSessionCompleted found with expected date")
        self.assertEqual(session_completed.exercises_completed.filter(weight=10).count(), 1,
                         "Expected to find 1 exercise for the completed session")

    def test_register_session_completed_with__string_for_date_raises_error(self):
        response = self.client.post(reverse('complete_session', kwargs={'session_id': self.training_session.id}), data={
            'date_completed': 'coucou',
            'form-0-weight': 10,
            'form-0-comment': 'commentaire qualitatif',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form_MAX_FORMS': '1000',
        })

        self.assertFormError(
            response,
            'session_completed_form',
            'date_completed',
            'Saisissez une date valide.'
        )

    def test_register_session_completed_with_string_for_weight_raises_error(self):
        response = self.client.post(reverse('complete_session', kwargs={'session_id': self.training_session.id}), data={
            'date_completed': '2020-04-03',
            'form-0-weight': 'coucou',
            'form-0-comment': 'commentaire qualitatif',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form_MAX_FORMS': '1000',
        })

        self.assertFormsetError(
            response,
            'exercise_completed_formset',
            0,
            'weight',
            'Saisissez un nombre entier.'
        )
