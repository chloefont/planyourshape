from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from muscu_site.models import TrainingSession, Exercise, TrainingSessionCompleted, ExerciseCompleted

import pdb


class LoggedInUserMixin(TestCase):

    def setUp(self):
        User.objects.create_user(
            username="patrick",
            password="right password"
        )

        self.client.login(username="patrick", password="right password")


class SessionListTest(LoggedInUserMixin):

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


class SessionCreationTest(LoggedInUserMixin):

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


class SessionCompleteTest(LoggedInUserMixin):

    def setUp(self):
        super().setUp()
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


class SessionSummaryTest(LoggedInUserMixin):

    def setUp(self):
        super().setUp()
        training_session = TrainingSession.objects.create(
            session_title='Ma Session',
            date='2020-01-01'
        )
        exercise_1 = Exercise.objects.create(
            exercise='Exercice 1',
            training_session=training_session
        )
        exercise_2 = Exercise.objects.create(
            exercise='Exercice 2',
            training_session=training_session
        )

        self.training_session_completed = TrainingSessionCompleted.objects.create(
            training_session=training_session,
            date_completed='2020-04-03'
        )
        ExerciseCompleted.objects.create(
            training_session_completed=self.training_session_completed,
            exercise=exercise_1,
        )
        ExerciseCompleted.objects.create(
            training_session_completed=self.training_session_completed,
            exercise=exercise_2,
        )

    def test_all_exercises_displayed(self):
        response = self.client.get(reverse('session_summary', kwargs={
            'session_completed_id': self.training_session_completed.id
        }))

        self.assertIn('exercises_completed', response.context[0])
        data = response.context['exercises_completed']

        self.assertEqual(data[0].exercise.exercise, 'Exercice 1')
        self.assertEqual(data[1].exercise.exercise, 'Exercice 2')


class LoginTest(LoggedInUserMixin):

    def setUp(self):
        self.user = User.objects.create_user(
            username="patrick",
            password="right password"
        )

    def test_right_login_input(self):
        response = self.client.post(reverse('login'), data={
            'username': "patrick",
            'password': "right password"
        }, follow=True)

        self.assertTrue(response.context['user'] == self.user)

    def test_wrong_login_input(self):
        response = self.client.post(reverse('login'), data={
            'username': "patrick",
            'password': "wrong password"
        })

        self.assertContains(response, "Le nom d'utilisateur ou le mot de passe entré n'est pas correct.")

    def test_wrong_access_to_login_required_page(self):
        response = self.client.get(reverse('create_session'))

        self.assertRedirects(response, '/?next=/sessions/create/')

    # def test_redirect_if_already_login(self):
    #     self.client.login(username="patrick", password="right password")
    #     response = self.client.get(reverse('login'))
    #
    #     self.assertRedirects(response, reverse('sessions_list'))

    def test_login_user_can_access_protected_page(self):
        self.client.login(username="patrick", password="right password")
        response = self.client.get(reverse('create_session'))

        self.assertEqual(response.status_code, 200)


class MenuTest(LoggedInUserMixin):

    def test_navbar_contains_sessions_list_link(self):
        response = self.client.get(reverse('sessions_list'))

        self.assertContains(response, '<a href="%s">Liste des séances</a>' % reverse('sessions_list'), html=True)

    def test_navbar_contains_session_creation_link(self):
        response = self.client.get(reverse('sessions_list'))

        self.assertContains(response, '<a href="%s">Créer une séance</a>' % reverse('create_session'), html=True)


class LogoutTest(LoggedInUserMixin):

    def test_navbar_contains_logout_link(self):
        response = self.client.get(reverse('sessions_list'))

        self.assertContains(response, '<a href="%s">Se déconnecter</a>' % reverse('logout'), html=True)

    def test_logout_user_cannot_access_protected_page(self):
        response = self.client.get(reverse('logout')).path
        login_page = self.client.get(reverse('login')).path
        # pdb.set_trace()
        # response = self.client.get(reverse('sessions_list'))

        self.assertTrue(response == login_page)
