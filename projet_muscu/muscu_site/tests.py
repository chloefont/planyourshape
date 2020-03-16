import datetime

from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .forms import SessionForm, ExerciseForm

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
