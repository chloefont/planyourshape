from django.db import models
from django.utils import timezone


class TrainingSession(models.Model):
    label = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.label

class Exercice(models.Model):
    training_session = models.ForeignKey(
        TrainingSession, on_delete=models.CASCADE, related_name='exercice'
    )
    label = models.CharField(max_length=100)
    sets = models.DateTimeField(default=1)
    reps = models.IntegerField(default=1)
    break_time = models.IntegerField(default=60)

    def __str__(self):
        return self.label
