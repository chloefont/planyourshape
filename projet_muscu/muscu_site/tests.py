from django.test import TestCase
from django.test import Client
from django.urls import reverse
from .models import TrainingSession, Exercice, SessionForm, ExerciceForm

class SessionCreationTest(TestCase):
    def test_date_in_future(self):
        self.client = Client()
        self.client.post(reverse('session_creation'), data={
            'session_title': 'Ma Session',
            'date': '10.01.2050',
            'form-TOTAL_FORMS': '3',
            'form-INITIAL_FORMS': '0',
            'form-MAX_NUM_FORMS': '10',
        })
